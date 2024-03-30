export const LOGIN_ENDPOINT = `${process.env.NEXT_PUBLIC_GATEWAY_URL}/login`;
export const VALIDATE_TOKEN_ENDPOINT = `${process.env.NEXT_PUBLIC_SERVER_SIDE_GATEWAY_URL ? process.env.NEXT_PUBLIC_SERVER_SIDE_GATEWAY_URL : process.env.NEXT_PUBLIC_GATEWAY_URL}/validate-token`;
export const QUEUE_ENDPOINT = `${process.env.NEXT_PUBLIC_GATEWAY_URL}/queue`;
export const ITEMS_ENDPOINT = `${process.env.NEXT_PUBLIC_GATEWAY_URL}/items`;
export const TERMINATE_ENDPOINT = `${process.env.NEXT_PUBLIC_GATEWAY_URL}/terminate`;
export const RETRY_ENDPOINT = `${process.env.NEXT_PUBLIC_GATEWAY_URL}/retry`;
export const DOWNLOAD_ENDPOINT = `${process.env.NEXT_PUBLIC_GATEWAY_URL}/download`;
