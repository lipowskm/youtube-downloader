import { Alert, Center, Text } from "@mantine/core";
import { AlertCircle } from "tabler-icons-react";
import React from "react";

interface AlertErrorProps {
  message: string;
  styles?: React.CSSProperties;
}

export const AlertError = (props: AlertErrorProps) => {
  return (
    <div {...(props.styles ? { style: props.styles } : {})}>
      <Alert icon={<AlertCircle size="1rem" />} color="red" variant="light">
        <Center>
          <Text fw={700}>{props.message}</Text>
        </Center>
      </Alert>
    </div>
  );
};
