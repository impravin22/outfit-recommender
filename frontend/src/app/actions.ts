'use server'

import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export async function analyzeOutfit(formData: FormData) {
  const query = formData.get('query') as string
  const file = formData.get('image') as File

  if (!file) {
    return { error: 'No file uploaded' }
  }

  // Log the request to Prisma (SQLite)
  try {
    await prisma.requestLog.create({
      data: {
        query: query || 'Default Query',
      },
    })
  } catch (e) {
    console.error("Failed to log to DB:", e)
    // Don't fail the whole request if logging fails
  }

  // Call Flask Backend
  // Use internal service name when in Docker/Podman network
  const backendUrl = process.env.BACKEND_INTERNAL_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api'
  
  try {
    const response = await fetch(`${backendUrl}/analyze`, {
      method: 'POST',
      body: formData,
      // Next.js server actions automatically handle FormData boundaries
    })

    if (!response.ok) {
      const errorText = await response.text()
      return { error: `Backend error: ${response.status} - ${errorText}` }
    }

    const data = await response.json()
    return data

  } catch (error) {
    console.error("Error calling backend:", error)
    return { error: "Failed to connect to analysis service." }
  }
}
