"use client";

import { Button, Flex } from "@chakra-ui/react";
import axios from "axios";
import { useRouter } from "next/navigation";

import { deleteCookie, getCookies } from "../utils";

export default function Page() {
  const router = useRouter()
  const onClick = async () => {
    const r = await axios.get("http://localhost:8080/test", {
      withCredentials: true,
    });
    console.log(r);
  };

  const onLogout = () => {
    document.cookie = "JWT=";
    router.push('/login')
    //TODO revoke token on the backend
  };
  //   getCookies().then((r) => {
  //     console.log(r);
  //   });

  return (
    <Flex direction="column" alignItems="center" gap={2}>
      <Button onClick={onClick} width="min-content">
        CLICK ME
      </Button>
      <Button onClick={onLogout} width="min-content">
        LOG OUT
      </Button>
    </Flex>
  );
}
