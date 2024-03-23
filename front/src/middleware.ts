import axios from "axios";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";


export async function middleware(request: NextRequest) {
  const redirectionRef = NextResponse.redirect(new URL("/login", request.url));
  const jwt = request.cookies.get("JWT");
  if (!jwt) return redirectionRef;

  const resp = await fetch("http://localhost:8080/validate-token", {
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
