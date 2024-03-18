'use server'
 
import { cookies } from 'next/headers'

export async function getCookies() {
  const cookieStore = cookies()
  return cookieStore.getAll()
}

export async function deleteCookie(name: string) {
  const cookieStore = cookies()
  cookieStore.delete(name)
}