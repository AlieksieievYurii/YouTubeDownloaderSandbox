"use client"

import { defineStyle, defineStyleConfig } from "@chakra-ui/react";
import { extendTheme } from "@chakra-ui/react";

const outline = defineStyle({
  border: "5px dashed", // change the appearance of the border
  borderRadius: 0, // remove the border radius
  fontWeight: "semibold", // change the font weight
});

export const buttonTheme = defineStyleConfig({
  variants: { outline },
});

export const theme = extendTheme({
  components: { Button: buttonTheme },
});