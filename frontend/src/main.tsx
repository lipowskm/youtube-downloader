import React, { useMemo, useState } from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import {
  ColorScheme,
  ColorSchemeProvider,
  MantineProvider,
} from "@mantine/core";

function Main() {
  const [colorScheme, setColorScheme] = useState<ColorScheme>("dark");
  const toggleColorScheme = (value?: ColorScheme) => {
    const theme = value || (colorScheme === "dark" ? "light" : "dark");
    localStorage.setItem("theme", theme);
    setColorScheme(theme);
  };

  useMemo(() => {
    const theme = localStorage.getItem("theme") as ColorScheme;
    if (theme) toggleColorScheme(theme);
    else localStorage.setItem("theme", "dark");
  }, []);

  return (
    <ColorSchemeProvider
      colorScheme={colorScheme}
      toggleColorScheme={toggleColorScheme}
    >
      <MantineProvider
        theme={{ ...{ colorScheme }, white: "#F2F2F2" }}
        withGlobalStyles
        withNormalizeCSS
      >
        <App />
      </MantineProvider>
    </ColorSchemeProvider>
  );
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <Main />
  </React.StrictMode>
);
