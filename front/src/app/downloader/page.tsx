"use client";
import { CloseIcon, DeleteIcon, DownloadIcon, RepeatIcon, WarningTwoIcon } from "@chakra-ui/icons";
import { Link } from "@chakra-ui/next-js";
import { Button, Flex, IconButton, Input, Progress, Spinner, Text, useToast } from "@chakra-ui/react";
import axios from "axios";
import { useEffect, useRef, useState } from "react";

import { ITEMS_ENDPOINT, QUEUE_ENDPOINT } from "@/config";

interface Item {
  url: string;
  video_id: string;
  state: State;
  error_message: string | undefined;
  progress: number;
  total_size: number;
  downloaded_size: number;
}

enum State {
  DOWNLOADED = "DOWNLOADED",
  DOWNLOADING = "DOWNLOADING",
  QUEUED = "QUEUED",
  FAILED = "FAILED",
}

const Item = ({ item }: { item: Item }) => {
  let progress_bar = null;
  if (item.state === State.QUEUED || item.state === State.DOWNLOADING) {
    progress_bar = <Progress width="100%" size="xs" isIndeterminate mt={2} />;
  }

  let hint = "Pending...";
  if (item.state === State.DOWNLOADING) {
    hint = `${item.progress} % (${item.downloaded_size / 1000000} / ${item.total_size / 1000000} MB)`;
  } else if (item.state === State.DOWNLOADED) {
    hint = "34.4 MB";
  } else if (item.state === State.FAILED) {
    hint = item.error_message || "No error message";
  }

  const onCancel = () => {
    console.log("Cancel");
  };

  const onDelete = () => {
    console.log("Delete");
  };

  const onRetry = () => {
    console.log("Retry");
  };

  const onDownload = () => {};

  let action = (
    <IconButton aria-label="Cancel" icon={<CloseIcon />} colorScheme="blue" onClick={onCancel} />
  );
  if (item.state === State.DOWNLOADED)
    action = (
      <Flex gap={1}>
        <IconButton
          aria-label="Delete"
          icon={<DeleteIcon />}
          colorScheme="red"
          onClick={onDelete}
        />
        <IconButton
          aria-label="Download"
          icon={<DownloadIcon />}
          colorScheme="blue"
          onClick={onDownload}
        />
      </Flex>
    );
  else if (item.state === State.FAILED)
    action = (
      <IconButton
        aria-label="Cancel"
        icon={<RepeatIcon />}
        colorScheme="orange"
        onClick={onRetry}
      />
    );

  return (
    <Flex mt={3} borderRadius="xl" direction="column" bg="gray.100" p={3}>
      <Flex justifyContent="space-between" alignItems="center" gap={2}>
        <Link href={item.url}>{item.url}</Link>
        <Text maxWidth="50%" as="i">
          {hint}
        </Text>
        {action}
      </Flex>
      {progress_bar}
    </Flex>
  );
};

const data = [
  { video_id: "0", url: "http://0", state: "FAILED", error_message: "No space" },
  {
    video_id: "1",
    url: "http://1",
    state: "DOWNLOADING",
    progress: 50,
    downloaded_size: 1000000,
    total_size: 2000000,
  },
  { video_id: "2", url: "http://2", state: "DOWNLOADED" },
  { video_id: "3", url: "http://3", state: "QUEUED" },
  {
    video_id: "4",
    url: "http://4",
    state: "DOWNLOADING",
    progress: 34,
    total_size: 2000000,
    downloaded_size: 1000000,
  },
  { video_id: "5", url: "http://5", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
  { video_id: "6", url: "http://6", state: "DOWNLOADING" },
];

export default function Page() {
  const [isPosting, setIsPosting] = useState(false);
  const [isLoadingItems, setIsLoadingItems] = useState(true);
  const [invalidInput, setInvalidInput] = useState<string | null>(null);
  const [items, setItems] = useState<Item[]>([]);
  const nameInput = useRef<HTMLInputElement>(null);
  const toast = useToast()

  const youTubeUrlRegex = /https:\/\/www\.youtube\.com\/watch\?v=(\S+)/;

  async function onQueue() {
    const target_url = nameInput.current!!.value;
    if (!youTubeUrlRegex.test(target_url)) {
      setInvalidInput("Invalid YouTube video URL!");
      return;
    }

    setIsPosting(true);
    axios
      .post(
        QUEUE_ENDPOINT,
        {
          youtube_url: target_url,
        },
        {
          withCredentials: true,
        },
      )
      .then((response) => {
        console.log(response);
        setIsPosting(false);
      })
      .catch((error) => {
        setIsPosting(false);
        console.log(error);
        toast({
          title: error.response.data,
          status: "error",
          position: "top",
          duration: null,
          isClosable: true,
        })
      });
  }

  const onInputChange = () => {
    setInvalidInput(null)
  }

  useEffect(() => {
    setIsLoadingItems(false);
    axios
      .get<Item[]>(ITEMS_ENDPOINT, {
        withCredentials: true,
      })
      .then((response) => {
        setItems(response.data);
        setIsLoadingItems(false);
      })
      .catch((error) => {
        console.log(`Failed to load items: ${error}`)
        toast({
          title: `Failed to load items!`,
          status: "error",
          position: "top",
          duration: null,
          isClosable: true,
        })
      });
  }, []);

  return (
    <Flex p={10} justifyContent="center">
      <Flex
        boxShadow="lg"
        borderRadius="xl"
        direction="column"
        overflow="hidden"
        width="100%"
        maxWidth="1000px"
      >
        <Flex direction="column" zIndex={1} boxShadow="lg" p={10} pb={5} bg="gray.100">
          <Flex direction="row" gap={2}>
            <Input
              borderColor="gray"
              colorScheme="white"
              variant="filled"
              placeholder="YouTube URL..."
              ref={nameInput}
              isInvalid={invalidInput !== null}
              onChange={onInputChange}
            ></Input>
            <Button colorScheme="green" isLoading={isPosting} onClick={onQueue}>
              Download
            </Button>
          </Flex>
          {invalidInput !== null ? (
            <Flex alignItems="center" mt={2}>
              <WarningTwoIcon color="red" />
              <Text ml={2} color="red">
                {invalidInput}
              </Text>
            </Flex>
          ) : (
            <></>
          )}
        </Flex>

        <Flex direction="column" px={4} maxHeight="50vh" overflow="auto">
          {isLoadingItems ? (
            <Flex width="100%" justifyContent="center" pt={10} pb={10}>
              <Spinner
                thickness="4px"
                speed="0.65s"
                emptyColor="gray.200"
                color="blue.500"
                size="xl"
              />
            </Flex>
          ) : (
            data.map((it) => <Item key={it.video_id} item={it} />)
          )}
        </Flex>
      </Flex>
    </Flex>
  );
}
