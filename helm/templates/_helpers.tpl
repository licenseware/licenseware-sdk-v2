{{/*
Expand the name of the chart.
*/}}
{{- define "<CHARTNAME>.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "<CHARTNAME>.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "<CHARTNAME>.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "<CHARTNAME>.labels" -}}
helm.sh/chart: {{ include "<CHARTNAME>.chart" . }}
{{ include "<CHARTNAME>.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "<CHARTNAME>.selectorLabels" -}}
app.kubernetes.io/name: {{ include "<CHARTNAME>.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{ include "<CHARTNAME>.appDefinition" . }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "<CHARTNAME>.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "<CHARTNAME>.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.service" -}}
{{- if .Values.service }}
  {{- toYaml .Values.service }}
{{- else -}}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.appName" -}}
{{ trimSuffix "-service" .Chart.Name }}
{{- end }}

{{- define "<CHARTNAME>.appDefinition" -}}
licenseware.io/app: {{ include "<CHARTNAME>.appName" . }}
licenseware.io/env: {{ .Values.metadata.env }}
licenseware.io/tier: {{ .Values.metadata.tier }}
licenseware.io/owner: {{ .Values.metadata.owner }}
{{- end -}}

{{/*
Always pull the latest image on production and otherwise, let the user choose
*/}}
{{- define "<CHARTNAME>.imagePullPolicy" -}}
{{- if contains "prod" .Values.metadata.env }}
{{- "Always" }}
{{- else }}
{{- default "IfNotPresent" .Values.image.pullPolicy }}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.webCommand" -}}
{{- if .Values.config.webCommand }}
{{- .Values.config.webCommand }}
{{- else -}}
uwsgi -M --http-socket=0.0.0.0:{{ .Values.service.containerPort }} -w main:app --processes=4 --enable-threads --threads=4
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.podAntiAffinity" -}}
{{- if .Values.affinity }}
  {{- toYaml .Values.affinity }}
{{- else -}}
podAntiAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
  - weight: 100
    podAffinityTerm:
      topologyKey: "kubernetes.io/hostname"
      labelSelector:
        matchLabels:
          {{- include "<CHARTNAME>.selectorLabels" . | nindent 10 }}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.livenessProbe" -}}
{{- if .Values.probes.livenessProbe }}
  {{- .Values.probes.livenessProbe }}
{{- else -}}
tcpSocket:
  port: 5000
initialDelaySeconds: 5
timeoutSeconds: 5
successThreshold: 1
failureThreshold: 3
periodSeconds: 10
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.appUriPrefix" -}}
{{- required "missing required value: .Values.config.appUriPrefix" .Values.config.appUriPrefix }}
{{- end }}

{{- define "<CHARTNAME>.defaultHealthcheckUri" -}}
{{- (list (include "<CHARTNAME>.appUriPrefix" .) "swagger.json") | join "/" }}
{{- end }}

{{- define "<CHARTNAME>.readinessProbe" -}}
{{- if .Values.probes.readinessProbe }}
  {{- .Values.probes.readinessProbe }}
{{- else -}}
httpGet:
  path: {{ default (include "<CHARTNAME>.defaultHealthcheckUri" .) .Values.config.healthCheckUri }}
  port: 5000
initialDelaySeconds: 5
timeoutSeconds: 2
successThreshold: 1
failureThreshold: 3
periodSeconds: 10
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.resources" -}}
{{- if .Values.resources }}
  {{- toYaml .Values.resources }}
{{- else -}}
requests:
  cpu: 100m
  memory: 128Mi
limits:
  cpu: 2000m
  memory: 8Gi
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.claimName" -}}
{{- if .Values.config.storage.claimName }}
{{- .Values.config.storage.claimName }}
{{- else }}
{{- .Chart.Name }}
{{- end }}
{{- end }}
