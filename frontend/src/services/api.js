export async function getPrediction(payload) {
  const res = await fetch("https://startup-funding-yohu.onrender.com/predict",
     {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text);
  }

  return res.json();
}
