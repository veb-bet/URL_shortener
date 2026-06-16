package main

import (
	"fmt"
	"net/http"
	"math/rand"
)

var storage = make(map[string]string)

func main() {
	http.HandleFunc("/shorten", shortenHandler)
	http.HandleFunc("/r/", redirectHandler)
	http.ListenAndServe(":8080", nil)
}

func shortenHandler(w http.ResponseWriter, r *http.Request) {
	url := r.URL.Query().Get("url")
	code := generateCode()
	storage[code] = url
	fmt.Fprintf(w, "http://localhost:8080/r/%s", code)
}

func redirectHandler(w http.ResponseWriter, r *http.Request) {
	code := r.URL.Path[3:]
	if dest, ok := storage[code]; ok {
		http.Redirect(w, r, dest, http.StatusFound)
	} else {
		http.NotFound(w, r)
	}
}

func generateCode() string {
	letters := []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
	b := make([]rune, 6)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}
