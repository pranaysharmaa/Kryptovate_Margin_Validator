import { Asset, MarginResponse } from "./types";

const API = "http://localhost:8000";

export async function fetchAssets(): Promise<Asset[]> {
  const res = await fetch(`${API}/config/assets`);
  const data = await res.json();
  return data.assets;
}

export async function validateMargin(payload: {
  asset: string;
  order_size: number;
  side: string;
  leverage: number;
  margin_client: number;
}): Promise<MarginResponse> {
  const res = await fetch(`${API}/margin/validate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}
