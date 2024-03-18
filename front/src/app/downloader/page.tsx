"use client";
import { CloseIcon } from "@chakra-ui/icons";
import { Link } from "@chakra-ui/next-js";
import { Button, Flex, IconButton, Input } from "@chakra-ui/react";

const Item = (props: { link: string }) => (
  <Flex
    mt={3}
    borderRadius="xl"
    direction="row"
    gap={2}
    bg="gray.100"
    justifyContent="space-between"
    p={3}
    alignItems="center"
  >
    <Link href="#">{props.link}</Link>
    <IconButton aria-label="Cancel" icon={<CloseIcon />} />
  </Flex>
);

const data = [
  { id: 0, link: "http://0" },
  { id: 1, link: "http://1" },
  { id: 2, link: "http://2" },
  { id: 3, link: "http://3" },
  { id: 4, link: "http://4" },
  { id: 5, link: "http://5" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
  { id: 6, link: "http://6" },
];

export default function Page() {
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
        <Flex direction="row" zIndex={1} boxShadow="lg" bg="gray.100" p={10} gap={2}>
          <Input borderColor="gray" colorScheme="white" variant="filled" placeholder="Filled"></Input>
          <Button colorScheme="green" isLoading>
            Download
          </Button>
        </Flex>
        <Flex direction="column" px={4} maxHeight="50vh" overflow="auto">
          {data.map((item) => (
            <Item key={item.id} link="http://lol.kek" />
          ))}
        </Flex>
      </Flex>
    </Flex>
  );
}
