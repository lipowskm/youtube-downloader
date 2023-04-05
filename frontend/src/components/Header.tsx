import {
  createStyles,
  Header as MantineHeader,
  rem,
  Group,
  Button,
  Title,
} from "@mantine/core";
import { ThemeToggleButton } from "./ThemeToggleButton";
import { BrandGithub } from "tabler-icons-react";

const useStyles = createStyles((theme) => ({
  header: {
    paddingLeft: theme.spacing.md,
    paddingRight: theme.spacing.md,
  },

  inner: {
    display: "flex",
    alignItems: "center",
    height: rem(56),

    [theme.fn.smallerThan("sm")]: {
      justifyContent: "flex-start",
    },
  },
}));

export function Header() {
  const { classes } = useStyles();

  return (
    <MantineHeader height={56} mb={120} className={classes.header}>
      <Group sx={{ height: "100%" }} position="apart" spacing={"xl"}>
        <Title order={2}>Media Grabber</Title>
        <Group sx={{ height: "100%" }} position="right" spacing={"xl"}>
          <Button
            leftIcon={<BrandGithub />}
            variant="default"
            component="a"
            target="_blank"
            rel="noopener noreferrer"
            href="https://github.com/lipowskm/youtube-downloader"
          >
            GitHub
          </Button>
          <ThemeToggleButton />
        </Group>
      </Group>
    </MantineHeader>
  );
}
