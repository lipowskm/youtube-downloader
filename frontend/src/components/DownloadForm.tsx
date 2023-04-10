import { Button, createStyles, Group, TextInput } from "@mantine/core";
import React, { FormEventHandler } from "react";
import { Download, BrandYoutube } from "tabler-icons-react";

interface DownloadFormProps {
  inputValue: string;
  inputOnChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: FormEventHandler<HTMLFormElement>;
  downloadButtonDisabled: boolean;
  downloadButtonLoading: boolean;
}

const useStyles = createStyles((theme) => ({
  input: {
    width: "500px",
  },
  button: {
    transition: "background-color 0.2s ease-out, color 0.2s ease-out",
  },
}));

export function DownloadForm(props: DownloadFormProps) {
  const { classes } = useStyles();
  return (
    <form onSubmit={props.onSubmit}>
      <Group>
        <TextInput
          className={classes.input}
          value={props.inputValue}
          onChange={props.inputOnChange}
          placeholder="Paste the URL here"
          autoFocus
          icon={<BrandYoutube size="1.5rem" />}
          size={"lg"}
          radius={"lg"}
        />
        <Button
          type={"submit"}
          className={classes.button}
          leftIcon={<Download size="1.5rem" />}
          loading={props.downloadButtonLoading}
          disabled={props.downloadButtonDisabled}
          loaderPosition={"left"}
          size={"lg"}
          radius={"lg"}
        >
          Download
        </Button>
      </Group>
    </form>
  );
}
