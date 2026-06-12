package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os/exec"
	"strings"
)

type SystemInfo struct {
	Hostname   string  `json:"hostname"`
	OS         string  `json:"os"`
	CpuPercent float64 `json:"cpu_percent"`
	MemTotalMB int64   `json:"mem_total_mb"`
	MemUsedMB  int64   `json:"mem_used_mb"`
	MemFreeMB  int64   `json:"mem_free_mb"`
	BootTime   string  `json:"boot_time"`
}

type DiskInfo struct {
	Drive       string  `json:"drive"`
	TotalGB     float64 `json:"total_gb"`
	UsedGB      float64 `json:"used_gb"`
	FreeGB      float64 `json:"free_gb"`
	PercentUsed float64 `json:"percent_used"`
}

func System() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		info, err := getSystemInfo()
		if err != nil {
			jsonError(w, http.StatusInternalServerError, fmt.Sprintf("error obteniendo info del sistema: %v", err))
			return
		}
		jsonOK(w, info)
	}
}

func Disk() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		disks, err := getDiskInfo()
		if err != nil {
			jsonError(w, http.StatusInternalServerError, fmt.Sprintf("error obteniendo discos: %v", err))
			return
		}
		jsonOK(w, disks)
	}
}

func getSystemInfo() (*SystemInfo, error) {
	script := `
		$cpu = [math]::Round((Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average, 1)
		$os  = Get-CimInstance Win32_OperatingSystem
		[PSCustomObject]@{
			Hostname   = $env:COMPUTERNAME
			OS         = $os.Caption
			CpuPercent = $cpu
			MemTotalMB = [math]::Round($os.TotalVisibleMemorySize / 1024, 0)
			MemFreeMB  = [math]::Round($os.FreePhysicalMemory / 1024, 0)
			BootTime   = $os.LastBootUpTime.ToUniversalTime().ToString('o')
		} | ConvertTo-Json -Compress
	`
	out, err := runPS(script)
	if err != nil {
		return nil, err
	}

	var raw struct {
		Hostname   string  `json:"Hostname"`
		OS         string  `json:"OS"`
		CpuPercent float64 `json:"CpuPercent"`
		MemTotalMB int64   `json:"MemTotalMB"`
		MemFreeMB  int64   `json:"MemFreeMB"`
		BootTime   string  `json:"BootTime"`
	}
	if err := json.Unmarshal(out, &raw); err != nil {
		return nil, fmt.Errorf("parseando respuesta PS: %w", err)
	}

	return &SystemInfo{
		Hostname:   raw.Hostname,
		OS:         raw.OS,
		CpuPercent: raw.CpuPercent,
		MemTotalMB: raw.MemTotalMB,
		MemUsedMB:  raw.MemTotalMB - raw.MemFreeMB,
		MemFreeMB:  raw.MemFreeMB,
		BootTime:   raw.BootTime,
	}, nil
}

func getDiskInfo() ([]DiskInfo, error) {
	// Los nombres de campo deben coincidir con los json tags del struct (snake_case)
	script := `
		Get-PSDrive -PSProvider FileSystem |
		Where-Object { $_.Used -ne $null -and $_.Root -match '^[A-Z]:\\$' } |
		ForEach-Object {
			$total = $_.Used + $_.Free
			[PSCustomObject]@{
				drive        = $_.Root
				total_gb     = [math]::Round($total / 1GB, 2)
				used_gb      = [math]::Round($_.Used / 1GB, 2)
				free_gb      = [math]::Round($_.Free / 1GB, 2)
				percent_used = if ($total -gt 0) { [math]::Round($_.Used / $total * 100, 1) } else { 0 }
			}
		} | ConvertTo-Json -Compress
	`
	out, err := runPS(script)
	if err != nil {
		return nil, err
	}

	// ConvertTo-Json devuelve objeto si hay 1 disco, array si hay varios
	out = normalizeJSONArray(out)

	var disks []DiskInfo
	if err := json.Unmarshal(out, &disks); err != nil {
		return nil, fmt.Errorf("parseando discos: %w", err)
	}
	return disks, nil
}

// runPS ejecuta un script de PowerShell y devuelve stdout en UTF-8.
// PS 5.1 en pipe usa ASCII por defecto; forzamos UTF-8 en cada invocación.
func runPS(script string) ([]byte, error) {
	const utf8Prefix = "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8\n" +
		"$OutputEncoding = [System.Text.Encoding]::UTF8\n"
	cmd := exec.Command("powershell", "-NoProfile", "-NonInteractive", "-Command", utf8Prefix+script)
	out, err := cmd.Output()
	if err != nil {
		return nil, fmt.Errorf("powershell: %w", err)
	}
	return []byte(strings.TrimSpace(string(out))), nil
}

// normalizeJSONArray envuelve en array si PS devolvio un objeto unico.
func normalizeJSONArray(data []byte) []byte {
	s := strings.TrimSpace(string(data))
	if len(s) > 0 && s[0] == '{' {
		return []byte("[" + s + "]")
	}
	return data
}
