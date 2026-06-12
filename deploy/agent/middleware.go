package main

import (
	"crypto/subtle"
	"encoding/json"
	"net/http"
)

// authMiddleware valida el token en cada request.
// Acepta Authorization: Bearer <token>  o  X-Vigex-Token: <token>
func authMiddleware(token string) func(http.Handler) http.Handler {
	tokenBytes := []byte(token)
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			received := extractToken(r)
			if received == "" || subtle.ConstantTimeCompare([]byte(received), tokenBytes) != 1 {
				w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusUnauthorized)
			json.NewEncoder(w).Encode(map[string]string{"error": "token invalido o ausente"})
				return
			}
			next.ServeHTTP(w, r)
		})
	}
}

func extractToken(r *http.Request) string {
	if h := r.Header.Get("Authorization"); h != "" {
		if len(h) > 7 && h[:7] == "Bearer " {
			return h[7:]
		}
	}
	return r.Header.Get("X-Vigex-Token")
}
