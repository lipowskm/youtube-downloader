export enum JobStatus {
  Queued = "queued",
  Finished = "finished",
  Failed = "failed",
  Started = "started",
  Deferred = "deferred",
  Scheduled = "scheduled",
  Stopped = "stopped",
  Canceled = "canceled",
}
export interface WebsocketMessage {
  id: string;
  status: JobStatus;
  queue_position: number;
}

/**
 * Submit request to convert URL with media to API
 * @param url - url to video or playlist
 * @returns ID used to download file
 */
export const submitUrlConversion = async (url: string): Promise<string> => {
  let response;
  try {
    response = await fetch(
      "http://127.0.0.1:8000/convert?" + new URLSearchParams({ url }),
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
  } catch {
    throw Error("Unable to connect to API, please try again in a moment.");
  }
  if (response?.ok) {
    const result: { file_id: string } = await response.json();
    return result.file_id;
  } else {
    const result: { detail: string } = await response.json();
    throw Error(result.detail);
  }
};

export const downloadFile = (fileId: string): void => {
  let filename: string;
  fetch(`http://127.0.0.1:8000/file/${fileId}`, {
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => {
      const disposition = res.headers.get("Content-Disposition");
      filename = disposition!.split(/;(.+)/)[1].split(/=(.+)/)[1];
      if (filename.toLowerCase().startsWith("utf-8''"))
        filename = decodeURIComponent(filename.replace("utf-8''", ""));
      else filename = filename.replace(/['"]/g, "");
      return res.blob();
    })
    .then((blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
    });
};

interface NamedParameters {
  onClose?: (ev: CloseEvent) => any;
  onError?: (ev: Event) => any;
  onMessage?: (ev: MessageEvent) => any;
  onOpen?: (ev: Event) => any;
}
export const notify = (
  fileId: string,
  {
    onClose = undefined,
    onError = undefined,
    onMessage = undefined,
    onOpen = undefined,
  }: NamedParameters
): WebSocket => {
  const ws = new WebSocket(`ws://127.0.0.1:8000/notify/${fileId}/ws`);
  ws.onclose = onClose!;
  ws.onerror = onError!;
  ws.onmessage = onMessage!;
  ws.onopen = onOpen!;
  return ws;
};
