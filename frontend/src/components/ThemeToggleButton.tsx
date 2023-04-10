import {
  useMantineColorScheme,
  SegmentedControl,
  Center,
  Box,
} from "@mantine/core";
import { Sun, Moon } from "tabler-icons-react";

export function ThemeToggleButton() {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();

  return (
    <SegmentedControl
      value={colorScheme}
      onChange={(value: "light" | "dark") => toggleColorScheme(value)}
      data={[
        {
          value: "light",
          label: (
            <Center>
              <Sun size="1rem" />
              <Box ml={10}>Light</Box>
            </Center>
          ),
        },
        {
          value: "dark",
          label: (
            <Center>
              <Moon size="1rem" />
              <Box ml={10}>Dark</Box>
            </Center>
          ),
        },
      ]}
    />
  );
}
