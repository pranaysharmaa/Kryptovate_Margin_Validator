import { useEffect, useState } from "react";

// Asset configuration from backend
interface Asset {
  symbol: string;
  mark_price: number;
  contract_value: number;
  allowed_leverage: number[];
}

// Response from margin validation endpoint
interface MarginResponse {
  status: "ok" | "error";
  margin_required?: number;
  message?: string;
}

const API_BASE = "http://localhost:8000";

export default function App() {

  const [assets, setAssets] = useState<Asset[]>([]);
  const [asset, setAsset] = useState<Asset | null>(null);


  const [orderSize, setOrderSize] = useState<string>("");
  const [side, setSide] = useState<"long" | "short">("long");
  const [leverage, setLeverage] = useState<number>(0);


  const [margin, setMargin] = useState<number>(0);
  const [result, setResult] = useState<MarginResponse | null>(null);

 
  const isInvalidOrderSize =
    orderSize !== "" && Number(orderSize) <= 0;

 
  useEffect(() => {
    fetch(`${API_BASE}/config/assets`)
      .then(res => res.json())
      .then(data => {
        const list: Asset[] = data.assets;
        setAssets(list);
        setAsset(list[0]);
        setLeverage(list[0].allowed_leverage[0]);
      });
  }, []);

  
  useEffect(() => {
    if (!asset || !orderSize || isInvalidOrderSize) {
      setMargin(0);
      return;
    }

    const calculated =
      (asset.mark_price *
        Number(orderSize) *
        asset.contract_value) /
      leverage;

    setMargin(Number(calculated.toFixed(2)));
  }, [asset, orderSize, leverage, isInvalidOrderSize]);

  // Submit order preview to backend with recomputed margin
  const submitOrderPreview = async () => {
    if (!asset || !orderSize || isInvalidOrderSize) return;

    // Recompute margin here to avoid stale React state
    const calculatedMargin =
      (asset.mark_price *
        Number(orderSize) *
        asset.contract_value) /
      leverage;

    const marginClient = calculatedMargin.toFixed(2);

    const res = await fetch(`${API_BASE}/margin/validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        asset: asset.symbol,
        order_size: orderSize,      // string to preserve precision?
        side,
        leverage,
        margin_client: marginClient // string, backend parses as Decimal?
      }),
    });

    const data: MarginResponse = await res.json();
    setResult(data);
  };

  if (!asset) return null;

  return (
    <div className="min-h-screen flex items-center justify-center bg-bg">
      <div className="w-full max-w-md bg-card border border-border rounded-xl p-6">
        <h1 className="text-xl font-semibold mb-1">Margin Preview</h1>
        <p className="text-sm text-muted mb-5">
          Initial margin calculator
        </p>

        {/* Asset selection */}
        <div className="flex gap-2 mb-4">
          {assets.map(a => (
            <button
              key={a.symbol}
              onClick={() => {
                setAsset(a);
                setLeverage(a.allowed_leverage[0]);
                setOrderSize("");
                setResult(null);
              }}
              className={`flex-1 py-2 rounded-lg border text-sm font-medium
                ${
                  a.symbol === asset.symbol
                    ? "border-primary bg-primary/20"
                    : "border-border"
                }`}
            >
              {a.symbol}
            </button>
          ))}
        </div>

        <Field label="Mark Price">
          <input value={asset.mark_price} disabled className="input" />
        </Field>

        <Field label="Contract Value">
          <input value={asset.contract_value} disabled className="input" />
        </Field>

        <Field label="Order Size">
          <input
            type="number"
            value={orderSize}
            onChange={(e) => setOrderSize(e.target.value)}
            className={`input ${
              isInvalidOrderSize ? "border-error" : ""
            }`}
          />
          {isInvalidOrderSize && (
            <p className="mt-1 text-xs text-error">
              Order size must be greater than zero. This order may not be validated.
            </p>
          )}
        </Field>

        <Field label="Side">
          <select
            value={side}
            onChange={(e) =>
              setSide(e.target.value as "long" | "short")
            }
            className="input"
          >
            <option value="long">Long</option>
            <option value="short">Short</option>
          </select>
        </Field>

        <Field label="Leverage">
          <select
            value={leverage}
            onChange={(e) =>
              setLeverage(Number(e.target.value))
            }
            className="input"
          >
            {asset.allowed_leverage.map(l => (
              <option key={l} value={l}>
                {l}x
              </option>
            ))}
          </select>
        </Field>

        <div className="bg-black/40 rounded-lg p-4 my-4 flex justify-between">
          <span className="text-muted text-sm">Required Margin</span>
          <span className="text-lg font-semibold">{margin}</span>
        </div>

        <button
          onClick={submitOrderPreview}
          disabled={!orderSize || isInvalidOrderSize}
          className="w-full bg-primary py-2 rounded-lg font-medium disabled:opacity-50"
        >
          Submit Order Preview
        </button>

        {result && (
          <div
            className={`mt-4 p-3 rounded-lg text-sm border
              ${
                result.status === "ok"
                  ? "bg-success/20 border-success"
                  : "bg-error/20 border-error"
              }`}
          >
            {result.status === "ok"
              ? `Margin accepted (Required: ${result.margin_required})`
              : `${result.message} (Required: ${result.margin_required})`}
          </div>
        )}
      </div>
    </div>
  );
}

// Simple layout - reusable
function Field({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="mb-3">
      <label className="text-xs text-muted">{label}</label>
      {children}
    </div>
  );
}
