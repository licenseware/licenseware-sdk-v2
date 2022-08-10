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
{{- define "<CHARTNAME>.baseLabels" -}}
helm.sh/chart: {{ include "<CHARTNAME>.chart" . }}
{{ include "<CHARTNAME>.baseSelectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "<CHARTNAME>.baseSelectorLabels" -}}
app.kubernetes.io/name: {{ include "<CHARTNAME>.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{ toYaml .Values.commonLabels }}
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

{{- define "<CHARTNAME>.appName" -}}
{{- trimSuffix "-service" .Chart.Name }}
{{- end }}

{{- define "<CHARTNAME>.dashboardAppLabels" -}}
{{- include "<CHARTNAME>.baseLabels" . }}
{{ toYaml $.Values.dashboardApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.dashboardAppSelectorLabels" -}}
{{- include "<CHARTNAME>.baseSelectorLabels" . }}
{{ toYaml $.Values.dashboardApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.webAppLabels" -}}
{{- include "<CHARTNAME>.baseLabels" . }}
{{ toYaml .Values.webApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.webAppSelectorLabels" -}}
{{- include "<CHARTNAME>.baseSelectorLabels" . }}
{{ toYaml .Values.webApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.workerAppLabels" -}}
{{- include "<CHARTNAME>.baseLabels" . }}
{{ toYaml .Values.workerApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.workerAppSelectorLabels" -}}
{{- include "<CHARTNAME>.baseSelectorLabels" . }}
{{ toYaml .Values.workerApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.dashboardAppName" -}}
{{- include "<CHARTNAME>.fullname" . }}-dashboard
{{- end }}

{{- define "<CHARTNAME>.webAppName" -}}
{{- include "<CHARTNAME>.fullname" . }}-web
{{- end }}

{{- define "<CHARTNAME>.workerAppName" -}}
{{- include "<CHARTNAME>.fullname" . }}-worker
{{- end }}

{{- define "<CHARTNAME>.claimName" -}}
{{- if .Values.config.persistence.claimName }}
{{- .Values.config.persistence.claimName }}
{{- else }}
{{- .Chart.Name }}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.configName" -}}
{{- include "<CHARTNAME>.fullname" . }}-config
{{- end }}

{{- define "<CHARTNAME>.secretName" -}}
{{- include "<CHARTNAME>.fullname" . }}-secret
{{- end }}

{{- define "<CHARTNAME>.dashboardAppCommand" -}}
{{- if .Values.dashboardApp.command -}}
{{- .Values.dashboardApp.command }}
{{- else -}}
celery -A main:broker flower --address=0.0.0.0 --port={{ .Values.dashboardApp.service.containerPort }}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.webAppCommand" -}}
{{- if .Values.webApp.command -}}
{{- .Values.webApp.command }}
{{- else -}}
uwsgi -M --http-socket=0.0.0.0:{{ .Values.webApp.service.containerPort }} -w main:app --processes=4 --enable-threads --threads=4
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.workerAppCommand" -}}
{{- if .Values.workerApp.command -}}
{{- .Values.workerApp.command }}
{{- else -}}
celery -A main:broker worker -l info --concurrency=4 --autoscale=4,20
{{- end }}
{{- end }}


{{- define "<CHARTNAME>.env" -}}
{{- if .Values.env }}
{{- .Values.env }}
{{-  else if (hasKey .Values.commonLabels "licenseware.io/env") }}
{{- get .Values.commonLabels "licenseware.io/env" }}
{{- else }}
{{- default "prod" .Values.env }}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.dashboardAppLivenessProbePort" -}}
{{- if .Values.dashboardApp.probes.livenessProbe.tcpSocket }}
{{- if .Values.dashboardApp.probes.livenessProbe.tcpSocket.port }}
{{- .Values.dashboardApp.probes.livenessProbe.tcpSocket.port }}
{{- end }}
{{- else }}
{{- required "missing required value: .Values.dashboardApp.service.containerPort" .Values.dashboardApp.service.containerPort }}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.dashboardAppReadinessHttpPort" -}}
{{- if .Values.dashboardApp.probes.readinessProbe.httpGet }}
{{- if .Values.dashboardApp.probes.readinessProbe.httpGet.port }}
{{- .Values.dashboardApp.probes.readinessProbe.httpGet.port }}
{{- end }}
{{- else }}
{{- required "missing required value: .Values.dashboardApp.service.containerPort" .Values.dashboardApp.service.containerPort }}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.dashboardAppReadinessHttpPath" -}}
{{- if .Values.dashboardApp.probes.readinessProbe.httpGet }}
{{- if .Values.dashboardApp.probes.readinessProbe.httpGet.path }}
{{- .Values.dashboardApp.probes.readinessProbe.httpGet.path }}
{{- end }}
{{- else }}
{{- required "missing required value: .Values.dashboardApp.healthCheckUri" .Values.dashboardApp.healthCheckUri }}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.webAppLivenessProbePort" -}}
{{- if .Values.webApp.probes.livenessProbe.tcpSocket }}
{{- if .Values.webApp.probes.livenessProbe.tcpSocket.port }}
{{- .Values.webApp.probes.livenessProbe.tcpSocket.port }}
{{- end }}
{{- else }}
{{- required "missing required value: .Values.webApp.service.containerPort" .Values.webApp.service.containerPort }}
{{- end }}
{{- end }}

{{- define "<CHARTNAME>.webAppReadinessHttpPort" -}}
{{- required "missing required value: .Values.webApp.service.containerPort" .Values.webApp.service.containerPort }}
{{- end }}

{{- define "<CHARTNAME>.webAppReadinessHttpPath" -}}
{{- required "missing required value: .Values.webApp.healthCheckUri" .Values.webApp.healthCheckUri }}
{{- end }}

{{- define "<CHARTNAME>.redisPassword" -}}
{{- if .Values.redis.auth.password }}
{{- .Values.redis.auth.password }}
{{- else if .Values.secret.redis.password }}
{{- .Values.secret.redis.password }}
{{- end }}
{{- end }}
