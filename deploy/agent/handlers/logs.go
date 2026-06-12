package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
)

type LogEntry struct {
	Time    string `json:"time"`
	Level   string `json:"level"`
	Source  string `json:"source"`
	EventID int    `json:"event_id"`
	Message string `json:"message"`
}

func Logs() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		limitStr := r.URL.Query().Get("limit")
		limit := 50
		if limitStr != "" {
			if n, err := strconv.Atoi(limitStr); err == nil && n > 0 && n <= 500 {
				limit = n
			}
		}
		source := r.URL.Query().Get("source") // "Application", "System", "Security"
		if source == "" {
			source = "Application"
		}

		entries, err := getWindowsLogs(source, limit)
		if err != nil {
			jsonError(w, http.StatusInternalServerError, fmt.Sprintf("error leyendo Event Log: %v", err))
			return
		}
		jsonOK(w, map[string]any{"entries": entries, "source": source})
	}
}

func getWindowsLogs(source string, limit int) ([]LogEntry, error) {
	script := fmt.Sprintf(`
		Get-WinEvent -LogName '%s' -MaxEvents %d -ErrorAction SilentlyContinue |
		ForEach-Object {
			$level = switch ($_.Level) {
				1 { "critical" }
				2 { "error" }
				3 { "warning" }
				4 { "info" }
				default { "verbose" }
			}
			[PSCustomObject]@{
				time     = $_.TimeCreated.ToUniversalTime().ToString('o')
				level    = $level
				source   = $_.ProviderName
				event_id = $_.Id
				message  = ($_.Message -replace '\r?\n', ' ' -replace '\s+', ' ').Trim()[0..255] -join ''
			}
		} | ConvertTo-Json -Compress
	`, source, limit)

	out, err := runPS(script)
	if err != nil {
		return nil, err
	}
	if len(out) == 0 {
		return []LogEntry{}, nil
	}

	out = normalizeJSONArray(out)
	var entries []LogEntry
	if err := json.Unmarshal(out, &entries); err != nil {
		return nil, fmt.Errorf("parseando Event Log: %w", err)
	}
	return entries, nil
}
