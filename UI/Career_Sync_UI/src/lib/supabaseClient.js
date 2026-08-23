import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = supabaseUrl && supabaseAnonKey
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * Register a new user via the backend.
 * The backend handles Supabase sign-up, profile creation, and returns tokens if session exists.
 */
export async function registerUser(fullName, email, password) {
  const res = await fetch(`${API_BASE}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fullName, email, password }),
  })

  const data = await res.json()

  if (!res.ok) {
    // Throw with the backend's detail message for UI display / logging
    throw new Error(data.detail || 'Registration failed')
  }

  return data // { message, user, access_token, refresh_token, email_confirmation_required }
}

/**
 * Login with email and password. The backend returns profile info and tokens.
 */
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

/**
 * Verify OTP (used after email confirmation or passwordless login).
 * This uses Supabase client directly.
 */
export async function verifyOtp(email, token) {
  if (!supabase) {
    throw new Error('Supabase is not configured')
  }

  const { data, error } = await supabase.auth.verifyOtp({
    email,
    token,
    type: 'email',
  })

  if (error) {
    throw new Error(error.message)
  }

  return data
}

/**
 * Resend OTP / verification email.
 * Calls the backend endpoint which in turn asks Supabase to resend.
 */
export async function resendOtp(email) {
  const res = await fetch(`${API_BASE}/api/auth/resend-otp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  })

  const data = await res.json()

  if (!res.ok) {
    throw new Error(data.detail || 'Failed to resend OTP')
  }

  return data
}

/**
 * Check profile using an existing access token (e.g., after OAuth redirect).
 * Backend verifies the token and returns the user profile.
 */
export async function checkProfile(accessToken) {
  const res = await fetch(`${API_BASE}/api/session/check`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  })

  if (!res.ok) {
    throw new Error(`Session check failed: ${res.status}`)
  }

  return res.json()
}