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

{{- define "<CHARTNAME>.dashboardLabels" -}}
{{- include "<CHARTNAME>.baseLabels" . }}
{{ toYaml $.Values.dashboardApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.dashboardSelectorLabels" -}}
{{- include "<CHARTNAME>.baseSelectorLabels" . }}
{{ toYaml $.Values.dashboardApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.webLabels" -}}
{{- include "<CHARTNAME>.baseLabels" . }}
{{ toYaml .Values.webApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.webSelectorLabels" -}}
{{- include "<CHARTNAME>.baseSelectorLabels" . }}
{{ toYaml .Values.webApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.workerLabels" -}}
{{- include "<CHARTNAME>.baseLabels" . }}
{{ toYaml .Values.workerApp.labels }}
{{- end }}

{{- define "<CHARTNAME>.workerSelectorLabels" -}}
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

{{- define "<CHARTNAME>.dashboardCommand" -}}
{{- if .Values.dashboardApp.command -}}
{{- .Values.dashboardApp.command }}
{{- else -}}
uwsgi -M --http-socket=0.0.0.0:{{ .Values.webApp.service.containerPort }} -w main:app --processes=4 --enable-threads --threads=4
{{- end }}
{{- end }}
