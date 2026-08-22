import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = supabaseUrl && supabaseAnonKey
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Used by the OAuth callback page (session already exists client-side)
export async function checkProfile(accessToken) {
  const res = await fetch(`${API_BASE}/api/session/check`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  })
  if (!res.ok) throw new Error(`Session check failed: ${res.status}`)
  return res.json()
}

export async function verifyOtp(email, token) {
  const res = await fetch(`${API_BASE}/api/auth/verify-otp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, token }),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Verification failed')
  return data
}

export async function resendOtp(email) {
  const res = await fetch(`${API_BASE}/api/auth/resend-otp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Could not resend code')
  return data
}

// Used by the password login form — FastAPI does the Supabase call for us
export async function loginWithPassword(email, password) {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  const data = await res.json()
  if (!res.ok) {
    throw new Error(data.detail || 'Login failed')
  }
  return data
}