import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { VALIDATE_TOKEN_ENDPOINT } from "./config";

export async function middleware(request: NextRequest) {
  const redirectionRef = NextResponse.redirect(new URL("/login", request.url));
  const jwt = request.cookies.get("JWT");
  if (!jwt) return redirectionRef;

  const resp = await fetch(VALIDATE_TOKEN_ENDPOINT, {
    headers: {
      Cookie: `JWT=${jwt.value}`,
    },
  });
  if (resp.status != 200) return redirectionRef;
  return NextResponse.next();
}

export const config = {
  matcher: "/downloader",
};
