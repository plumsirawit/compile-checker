import React, { useRef, useState } from "react";
import logo from "./ITTT_logo_v1_square.png";
import "./App.css";
import { saveAs } from "file-saver";
import { Buffer } from "buffer";

function App() {
  const [passcode, setPasscode] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Automatic checker.cpp compiler</p>
        <input
          type="text"
          placeholder="passcode"
          onChange={(e) => setPasscode(e.target.value)}
        />
        <br />
        <input type="file" ref={fileInputRef} />
        <br />
        <input
          type="submit"
          onClick={async () => {
            const file = fileInputRef?.current?.files?.[0];
            if (!file) {
              alert("File not attached");
              return;
            }
            const text = await file.text();
            try {
              const resp = await fetch(
                "https://3ash30diz0.execute-api.ap-southeast-1.amazonaws.com/dev/compile",
                {
                  method: "post",
                  body: JSON.stringify({
                    secret: passcode,
                    source: text,
                  }),
                }
              );
              if (resp.status !== 200) {
                alert(`something is wrong (code is ${resp.status}, not 200).`);
                return;
              }
              const respJson = await resp.json();
              const buffer = Buffer.from(respJson.message, "base64");
              saveAs(
                new Blob([buffer], { type: "application/octet-stream" }),
                "checker"
              );
            } catch (e) {
              alert(e);
            }
          }}
        />
      </header>
    </div>
  );
}

export default App;
