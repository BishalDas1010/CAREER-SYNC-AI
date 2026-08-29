import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// detectSessionInUrl (on by default) is what lets supabase-js pick up the
// session automatically when the user lands back on /auth/callback after
// clicking the confirmation link.
export const supabase = supabaseUrl && supabaseAnonKey
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

/**
 * Register a new user via the backend.
 * Supabase sends a confirmation EMAIL LINK (not an OTP code) — the user
 * clicks it, lands on /auth/callback, and is sent to /login from there.
 */
export async function registerUser(fullName, email, password) {
  const res = await fetch(`${API_BASE}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fullName, email, password }),
  })

  const data = await res.json()

  if (!res.ok) {
    throw new Error(data.detail || 'Registration failed')
  }

  return data // { message, user, access_token, refresh_token, email_confirmation_required }
}

/**
 * Login with email and password. The backend returns profile info and tokens.
 * We also sync the tokens into the supabase-js client so subsequent
 * supabase.auth.* calls in the app (e.g. sign out) work correctly.
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

  if (supabase && data.access_token && data.refresh_token) {
    await supabase.auth.setSession({
      access_token: data.access_token,
      refresh_token: data.refresh_token,
    })
  }

  return data
}

/**
 * Resend the confirmation email if the user didn't get it / it expired.
 * This is a direct Supabase client call — no backend round trip needed.
 */
export async function resendConfirmationEmail(email) {
  if (!supabase) {
    throw new Error('Supabase is not configured')
  }

  const { error } = await supabase.auth.resend({
    type: 'signup',
    email,
    options: {
      emailRedirectTo: `${window.location.origin}/auth/callback`,
    },
  })

  if (error) {
    throw new Error(error.message)
  }

  return { message: 'Confirmation email resent.' }
}

/**
 * Call this on your /auth/callback page after the user clicks the
 * confirmation link. supabase-js (detectSessionInUrl) usually picks the
 * session up automatically, but some Supabase project configs use the
 * PKCE "code" flow instead — this handles both.
 */
export async function completeEmailConfirmation() {
  if (!supabase) {
    throw new Error('Supabase is not configured')
  }

  const params = new URLSearchParams(window.location.search)
  const code = params.get('code')

  if (code) {
    const { data, error } = await supabase.auth.exchangeCodeForSession(code)
    if (error) throw new Error(error.message)
    return data // { session, user }
  }

  // Implicit flow: session should already be set by detectSessionInUrl.
  const { data, error } = await supabase.auth.getSession()
  if (error) throw new Error(error.message)
  return data // { session }
}

/**
 * Check profile using an existing access token.
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