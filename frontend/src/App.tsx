import React, { useState } from "react";
import "./App.css";
import { DownloadForm } from "./components/DownloadForm";
import { Header } from "./components/Header";
import {
  downloadFile,
  JobStatus,
  notify,
  submitUrlConversion,
  WebsocketMessage,
} from "./services/ApiService";
import {
  AppShell,
  Center,
  Container,
  Space,
  Title,
  Text,
  Paper,
  Transition,
} from "@mantine/core";
import { AlertSuccess } from "./components/AlertSuccess";
import { AlertError } from "./components/AlertError";


function App() {
  const [inputUrl, setInputUrl] = useState("");
  const [urlValid, setUrlValid] = useState(false);
  const [readyToDownload, setReadyToDownload] = useState(true);
  const [fileUrl, setFileUrl] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const onMessage = (event: MessageEvent) => {
    const data: string = event.data;
    const message: WebsocketMessage = JSON.parse(data);
    if (
      [
        JobStatus.Finished,
        JobStatus.Canceled,
        JobStatus.Stopped,
        JobStatus.Failed,
      ].includes(message.status)
    ) {
      setReadyToDownload(true);
    }
    if (message.status == JobStatus.Finished) {
      downloadFile(message.id);
      setFileUrl(`http://127.0.0.1:8000/file/${message.id}`);
    } else {
      // TODO: Implement validation of URLs to prevent sending invalid URL to API
      //  (including URLs with valid syntax but pointing to non-existing video)
      //  ----------------------------------------------
      //  Also implement sending error messages from jobs
      //  to provide more information to the user. (on the backend side!)
      setErrorMessage(
        "Unable to download specified file, please check if the URL is valid."
      );
    }
  };

  const isValidUrl = (url: string): boolean => {
    try {
      const inputUrl = new URL(url);
      const domain = inputUrl.hostname.replace("www.", "").replace(".com", "");
      return ["youtube"].includes(domain.toLowerCase());
    } catch {
      return false;
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const input = e.currentTarget.value;
    setInputUrl(input);
    setUrlValid(isValidUrl(input));
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (!readyToDownload) {
      return;
    }
    setReadyToDownload(false);
    setFileUrl("");
    setErrorMessage("");
    submitUrlConversion(inputUrl)
      .then((fileId) => {
        notify(fileId, { onMessage: onMessage });
      })
      .catch((err: Error) => {
        setErrorMessage(err.message);
        setReadyToDownload(true);
      });
  };

  return (
    <AppShell padding={"md"} fixed={false} header={<Header />}>
      <Container>
        <Center>
          <Title order={1}>
            One{" "}
            <Text
              span
              variant={"gradient"}
              gradient={{ from: "grape.4", to: "violet.4", deg: 45 }}
              inherit
            >
              tool
            </Text>{" "}
            to download them all
          </Title>
        </Center>
        <Space h="xl" />
        <Paper shadow="lg" p="md" radius={"lg"} withBorder>
          <Center>
            <DownloadForm
              inputValue={inputUrl}
              inputOnChange={handleInputChange}
              onSubmit={handleSubmit}
              downloadButtonLoading={!readyToDownload}
              downloadButtonDisabled={!urlValid}
            />
          </Center>
        </Paper>
        <Space h="xl" />
        <Transition
          mounted={
            readyToDownload && (fileUrl.length > 0 || errorMessage.length > 0)
          }
          transition="slide-down"
          duration={400}
          exitDuration={1}
          timingFunction="ease"
        >
          {(styles) =>
            (fileUrl.length > 0 && (
              <AlertSuccess styles={styles} fileUrl={fileUrl} />
            )) ||
            (errorMessage.length > 0 && (
              <AlertError styles={styles} message={errorMessage} />
            ))
          }
        </Transition>
      </Container>
    </AppShell>
  );
}

export default App;
