import axios from "axios";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

// This function can be marked `async` if using `await` inside
export async function middleware(request: NextRequest) {
  const redirectionRef = NextResponse.redirect(new URL("/login", request.url));
  const jwt = request.cookies.get("JWT");
  console.log("DUPA")
  if (!jwt) return redirectionRef;

  const resp = await fetch("http://localhost:8080/validate-token", {
    headers: {
      Cookie: `JWT=${jwt.value}`,
    },
  });
  if (resp.status != 200) return redirectionRef;
  return NextResponse.next();
}

// // See "Matching Paths" below to learn more
export const config = {
  matcher: "/test",
};
