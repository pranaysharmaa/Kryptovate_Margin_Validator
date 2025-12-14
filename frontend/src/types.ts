export interface Asset {
  symbol: string;
  mark_price: number;
  contract_value: number;
  allowed_leverage: number[];
}

export interface MarginResponse {
  status: "ok" | "error";
  margin_required?: number;
  message?: string;
}
