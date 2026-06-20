const API_BASE_URL = "http://127.0.0.1:8000";

export async function checkBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Backend is not available");
  }

  return data;
}

export async function calculateScore(formData) {
  const response = await fetch(`${API_BASE_URL}/calculate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Score calculation failed");
  }

  return data;
}

export async function scoreHand(handData) {
  const response = await fetch(`${API_BASE_URL}/score-hand`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(handData),
  });

  const data = await response.json();

  if (!response.ok) {
    const message = data.errors?.join(" ") || data.error || "Hand scoring failed";
    throw new Error(message);
  }

  return data;
}
