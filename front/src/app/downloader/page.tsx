"use client";
import { CloseIcon, DeleteIcon, DownloadIcon, RepeatIcon, WarningTwoIcon } from "@chakra-ui/icons";
import { Link } from "@chakra-ui/next-js";
import {
  Button,
  Flex,
  IconButton,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
  Progress,
  Spinner,
  Text,
  useToast,
} from "@chakra-ui/react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import {
  DOWNLOAD_ENDPOINT,
  ITEMS_ENDPOINT,
  QUEUE_ENDPOINT,
  RETRY_ENDPOINT,
  TERMINATE_ENDPOINT,
} from "@/config";

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

const ConfirmationDialog = ({ target }: any) => {
  return (
    <>
      <Modal isOpen={target != null} onClose={target?.onCancel}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{target?.title}</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Text>{target?.description}</Text>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={target?.onCancel}>
              Cancel
            </Button>
            <Button variant="ghost" colorScheme="red" onClick={target?.onConfirm}>
              OK
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

const Item = ({
  item,
  onTerminate,
  onRetry,
}: {
  item: Item;
  onTerminate: (item: Item, showProcessing: () => void) => void;
  onRetry: (item: Item, done: () => void) => void;
}) => {
  const [loading, setLoading] = useState(false);
  const [retrying, setRetrying] = useState(false);

  let progress_bar = null;
  if (item.state === State.QUEUED || item.state === State.DOWNLOADING) {
    progress_bar = <Progress width="100%" size="xs" isIndeterminate mt={2} />;
  }

  let hint = "Pending...";
  if (item.state === State.DOWNLOADING) {
    hint = `${item.progress} % (${(item.downloaded_size / 1024 / 1024).toFixed(2)} / ${(item.total_size / 1024 / 1024).toFixed(2)} MB)`;
  } else if (item.state === State.DOWNLOADED) {
    hint = `${(item.total_size / 1024 / 1024).toFixed(2)} MB`;
  } else if (item.state === State.FAILED) {
    hint = item.error_message || "No error message";
  }

  let action = (
    <IconButton
      aria-label="Cancel"
      icon={<CloseIcon />}
      colorScheme="blue"
      isLoading={loading}
      onClick={() => {
        onTerminate(item, () => setLoading(true));
      }}
    />
  );
  if (item.state === State.DOWNLOADED)
    action = (
      <Flex gap={1}>
        <IconButton
          aria-label="Delete"
          isLoading={loading}
          icon={<DeleteIcon />}
          colorScheme="red"
          onClick={() => {
            onTerminate(item, () => setLoading(true));
          }}
        />
        <a href={`${DOWNLOAD_ENDPOINT}/${item.video_id}`}>
          <IconButton aria-label="Download" icon={<DownloadIcon />} colorScheme="blue" />
        </a>
      </Flex>
    );
  else if (item.state === State.FAILED)
    action = (
      <Flex gap={1}>
        <IconButton
          aria-label="Delete"
          icon={<DeleteIcon />}
          colorScheme="red"
          isLoading={loading}
          onClick={() => onTerminate(item, () => setLoading(true))}
        />
        <IconButton
          aria-label="Retry"
          icon={<RepeatIcon />}
          colorScheme="orange"
          isLoading={retrying}
          onClick={() => {
            setRetrying(true);
            onRetry(item, () => {
              setRetrying(false);
            });
          }}
        />
      </Flex>
    );

  return (
    <Flex mt={3} borderRadius="xl" direction="column" bg="gray.100" p={3}>
      <Flex justifyContent="space-between" alignItems="center" gap={2}>
        <Link href={item.url}>{item.video_id}</Link>
        <Text maxWidth="50%" as="i">
          {hint}
        </Text>
        {action}
      </Flex>
      {progress_bar}
    </Flex>
  );
};

export default function Page() {
  const [isPosting, setIsPosting] = useState(false);
  const [isLoadingItems, setIsLoadingItems] = useState(true);
  const [invalidInput, setInvalidInput] = useState<string | null>(null);
  const [items, setItems] = useState<Item[]>([]);
  const [targetConfirmation, setTargetConfirmation] = useState<any | null>(null);
  const nameInput = useRef<HTMLInputElement>(null);
  const toast = useToast();

  const youTubeUrlRegex = /https:\/\/www\.youtube\.com\/watch\?v=(\S{11})/;

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
        nameInput.current!!.value = "";
        toast({
          title: "Item has been queued",
          description: "Audio file will be downloaded soon",
          status: "success",
          position: "top",
          duration: 3000,
          isClosable: true,
        });
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
        });
      });
  }

  const onInputChange = () => {
    setInvalidInput(null);
  };

  const requestItems = (onResult: (items: Item[]) => void, onError: (error: string) => void) => {
    axios
      .get<Item[]>(ITEMS_ENDPOINT, {
        withCredentials: true,
      })
      .then((response) => {
        onResult(response.data);
      })
      .catch((error) => {
        console.log(`Failed to load items: ${error}`);
        onError(error);
      });
  };

  useEffect(() => {
    requestItems(
      (items) => {
        setItems(items);
        setIsLoadingItems(false);
      },
      (error) => {
        console.log(`Failed to load items: ${error}`);
        toast({
          title: `Failed to load items!`,
          status: "error",
          position: "top",
          duration: null,
          isClosable: true,
        });
      },
    );

    const id = setInterval(() => {
      requestItems(
        (items) => {
          setItems(items);
        },
        () => {
          console.log("Failed to update items");
        },
      );
    }, 3000);
    return () => clearInterval(id);
  }, []);

  const terminateItem = (item: Item, showProcessing: () => void) => {
    setTargetConfirmation({
      video_id: item.video_id,
      title: "Delete item",
      description: "Are you sure to delete?",
      onConfirm: () => {
        setTargetConfirmation(null);
        showProcessing();
        axios
          .delete(`${TERMINATE_ENDPOINT}/${item.video_id}`, { withCredentials: true })
          .catch((error) => {
            toast({
              title: error.response.data,
              status: "error",
              position: "top",
              duration: null,
              isClosable: true,
            });
          });
      },
      onCancel: () => {
        setTargetConfirmation(null);
      },
    });
  };

  const onRetry = (item: Item, done: () => void) => {
    axios
      .post(`${RETRY_ENDPOINT}/${item.video_id}`, {}, { withCredentials: true })
      .catch((error) => {
        toast({
          title: error.response.data,
          status: "error",
          position: "top",
          duration: null,
          isClosable: true,
        });
      })
      .finally(() => {
        done();
      });
  };

  return (
    <Flex p={10} alignItems="center" direction="column">
      <Text fontSize="4xl" mb={4}>
        Audio Downloader from YouTube
      </Text>
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
          ) : items.length != 0 ? (
            items.map((it) => (
              <Item key={it.video_id} item={it} onTerminate={terminateItem} onRetry={onRetry} />
            ))
          ) : (
            <Flex justifyContent="center" p={5}>
              <Text>No downloaded audios yet!</Text>
            </Flex>
          )}
        </Flex>
      </Flex>
      <ConfirmationDialog target={targetConfirmation} />
    </Flex>
  );
}
