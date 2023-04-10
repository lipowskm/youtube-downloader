import {
  ActionIcon,
  Alert,
  Anchor,
  Center,
  Group,
  Paper,
  Space,
  Text,
  Tooltip,
} from "@mantine/core";
import { Check, CircleCheck, Copy } from "tabler-icons-react";
import React from "react";
import { useClipboard } from "@mantine/hooks";

interface AlertSuccessProps {
  fileUrl: string;
  styles?: React.CSSProperties;
}

export const AlertSuccess = (props: AlertSuccessProps) => {
  const clipboard = useClipboard({ timeout: 1000 });

  return (
    <div {...(props.styles ? { style: props.styles } : {})}>
      <Alert icon={<CircleCheck size="1rem" />} color="green">
        <Center>
          <Text fw={700}>
            If the download doesn't start automatically, you can use the
            following link.
          </Text>
        </Center>
        <Space h="xs" />
        <Center>
          <Text fw={700}>It will be valid for 1 hour.</Text>
        </Center>
        <Space h="xs" />
        <Paper shadow="xs" p="xs" radius={"md"} withBorder>
          <Center>
            <Group>
              <Anchor href={props.fileUrl}>{props.fileUrl}</Anchor>
              <Tooltip
                label={
                  clipboard.copied ? (
                    <Center>
                      Copied&nbsp;
                      <Check size={18} strokeWidth={2} color={"teal"} />
                    </Center>
                  ) : (
                    "Copy to clipboard"
                  )
                }
                withArrow
                position="top"
              >
                <ActionIcon
                  variant="outline"
                  onClick={() => clipboard.copy(props.fileUrl)}
                >
                  <Copy size="1.125rem" />
                </ActionIcon>
              </Tooltip>
            </Group>
          </Center>
        </Paper>
        <Space h="xs" />
      </Alert>
    </div>
  );
};
