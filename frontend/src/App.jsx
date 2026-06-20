import { useEffect, useMemo, useState } from "react";
import {
  Calculator,
  CircleAlert,
  CircleCheck,
  Eraser,
  Plus,
  RotateCcw,
  Send,
  Sparkles,
  Trophy,
  X,
} from "lucide-react";
import { checkBackendHealth, scoreHand } from "./api.js";

const tileGroups = [
  {
    name: "Manzu",
    tiles: ["1m", "2m", "3m", "4m", "5m", "0m", "6m", "7m", "8m", "9m"],
  },
  {
    name: "Pinzu",
    tiles: ["1p", "2p", "3p", "4p", "5p", "0p", "6p", "7p", "8p", "9p"],
  },
  {
    name: "Souzu",
    tiles: ["1s", "2s", "3s", "4s", "5s", "0s", "6s", "7s", "8s", "9s"],
  },
  {
    name: "Honors",
    tiles: ["1z", "2z", "3z", "4z", "5z", "6z", "7z"],
  },
];

const allTiles = tileGroups.flatMap((group) => group.tiles);
const windOptions = ["east", "south", "west", "north"];

const conditionOptions = [
  { key: "riichi", label: "Riichi" },
  { key: "double_riichi", label: "Double riichi" },
  { key: "ippatsu", label: "Ippatsu" },
  { key: "rinshan", label: "Rinshan" },
  { key: "chankan", label: "Chankan" },
  { key: "haitei", label: "Haitei" },
  { key: "houtei", label: "Houtei" },
  { key: "tenhou", label: "Tenhou" },
  { key: "chiihou", label: "Chiihou" },
];

const initialHand = {
  tiles: [],
  winning_tile: "",
  win_type: "ron",
  winner_seat: "south",
  round_wind: "east",
  melds: [],
  dora_indicators: [],
  ura_dora_indicators: [],
  conditions: {},
  honba: 0,
  riichi_sticks: 0,
  rules: {
    has_aka_dora: true,
    has_open_tanyao: false,
    has_double_yakuman: true,
  },
};

function App() {
  const [hand, setHand] = useState(initialHand);
  const [selectedMeldTiles, setSelectedMeldTiles] = useState([]);
  const [meldType, setMeldType] = useState("chi");
  const [doraDraft, setDoraDraft] = useState("1m");
  const [uraDoraDraft, setUraDoraDraft] = useState("1m");
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState("checking");

  useEffect(() => {
    checkBackendHealth()
      .then(() => setBackendStatus("online"))
      .catch(() => setBackendStatus("offline"));
  }, []);

  const tileCounts = useMemo(() => countTiles(hand.tiles), [hand.tiles]);
  const uniqueHandTiles = useMemo(() => [...new Set(hand.tiles)], [hand.tiles]);
  const readinessMessages = useMemo(() => getReadinessMessages(hand), [hand]);
  const handReady = readinessMessages.length === 0;

  function updateHand(field, value) {
    setHand((currentHand) => ({ ...currentHand, [field]: value }));
    setError("");
  }

  function updateNumber(field, value) {
    const numberValue = Number(value);
    updateHand(field, Number.isNaN(numberValue) ? 0 : numberValue);
  }

  function addHandTile(tileId) {
    const normalId = normalizeRedFive(tileId);
    const currentCount = hand.tiles.filter((tile) => normalizeRedFive(tile) === normalId).length;
    if (currentCount >= 4 || hand.tiles.length >= 18) {
      return;
    }
    updateHand("tiles", [...hand.tiles, tileId]);
  }

  function removeHandTile(index) {
    const nextTiles = hand.tiles.filter((_, tileIndex) => tileIndex !== index);
    const nextWinningTile = nextTiles.some((tile) => normalizeRedFive(tile) === normalizeRedFive(hand.winning_tile))
      ? hand.winning_tile
      : "";
    setHand((currentHand) => ({
      ...currentHand,
      tiles: nextTiles,
      winning_tile: nextWinningTile,
      melds: [],
    }));
    setSelectedMeldTiles([]);
    setResult(null);
    setError("");
  }

  function toggleMeldSelection(tileId, index) {
    const selectionKey = `${tileId}-${index}`;
    const exists = selectedMeldTiles.some((tile) => tile.key === selectionKey);
    if (exists) {
      setSelectedMeldTiles(selectedMeldTiles.filter((tile) => tile.key !== selectionKey));
      return;
    }
    setSelectedMeldTiles([...selectedMeldTiles, { key: selectionKey, id: tileId }]);
  }

  function addMeld() {
    const neededCount = meldType === "kan" || meldType === "closed_kan" ? 4 : 3;
    if (selectedMeldTiles.length !== neededCount) {
      setError(`${formatMeldType(meldType)} needs exactly ${neededCount} selected tiles.`);
      return;
    }
    updateHand("melds", [
      ...hand.melds,
      { type: meldType, tiles: selectedMeldTiles.map((tile) => tile.id) },
    ]);
    setSelectedMeldTiles([]);
  }

  function removeMeld(index) {
    updateHand(
      "melds",
      hand.melds.filter((_, meldIndex) => meldIndex !== index)
    );
  }

  function addIndicator(field, tileId) {
    updateHand(field, [...hand[field], tileId]);
  }

  function removeIndicator(field, index) {
    updateHand(
      field,
      hand[field].filter((_, tileIndex) => tileIndex !== index)
    );
  }

  function toggleCondition(conditionKey) {
    updateHand("conditions", {
      ...hand.conditions,
      [conditionKey]: !hand.conditions[conditionKey],
    });
  }

  function resetAll() {
    setHand(initialHand);
    setSelectedMeldTiles([]);
    setResult(null);
    setError("");
  }

  function loadExampleHand() {
    setHand({
      ...initialHand,
      tiles: [
        "2m",
        "2m",
        "4m",
        "4m",
        "4m",
        "3p",
        "3p",
        "3p",
        "5p",
        "6p",
        "7p",
        "4s",
        "4s",
        "4s",
      ],
      winning_tile: "4s",
      conditions: { riichi: true },
    });
    setSelectedMeldTiles([]);
    setResult(null);
    setError("");
  }

  async function submitHand(event) {
    event.preventDefault();
    if (!handReady) {
      setError(readinessMessages.join(" "));
      return;
    }

    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const nextResult = await scoreHand(hand);
      setResult(nextResult);
    } catch (apiError) {
      setError(apiError.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="calculator-panel">
        <header className="top-bar">
          <div>
            <p className="eyebrow">Japanese riichi mahjong</p>
            <h1>Winning Hand Calculator</h1>
          </div>
          <BackendBadge status={backendStatus} />
        </header>

        <div className="workspace">
          <form className="score-form" onSubmit={submitHand}>
            <PanelTitle
              icon={<Calculator size={20} />}
              title="Enter the Winning Hand"
              subtitle={`${hand.tiles.length} of 14 tiles selected`}
            />

            <ReadinessPanel messages={readinessMessages} />

            <TileTray
              tiles={hand.tiles}
              winningTile={hand.winning_tile}
              selectedMeldTiles={selectedMeldTiles}
              onRemove={removeHandTile}
              onSelectForMeld={toggleMeldSelection}
            />

            <TilePalette tileCounts={tileCounts} onAddTile={addHandTile} />

            <label className="field">
              <span>Winning tile</span>
              <select
                value={hand.winning_tile}
                onChange={(event) => updateHand("winning_tile", event.target.value)}
              >
                <option value="">Choose from entered tiles</option>
                {uniqueHandTiles.map((tileId) => (
                  <option key={tileId} value={tileId}>
                    {getTileLabel(tileId)}
                  </option>
                ))}
              </select>
            </label>

            <div className="section-grid">
              <SegmentedControl
                label="Win type"
                value={hand.win_type}
                options={[
                  { label: "Ron", value: "ron" },
                  { label: "Tsumo", value: "tsumo" },
                ]}
                onChange={(value) => updateHand("win_type", value)}
              />

              <SelectField
                label="Winner seat"
                value={hand.winner_seat}
                options={windOptions}
                onChange={(value) => updateHand("winner_seat", value)}
              />

              <SelectField
                label="Round wind"
                value={hand.round_wind}
                options={windOptions}
                onChange={(value) => updateHand("round_wind", value)}
              />
            </div>

            <div className="field-grid">
              <NumberField
                label="Honba"
                min="0"
                value={hand.honba}
                onChange={(value) => updateNumber("honba", value)}
              />
              <NumberField
                label="Riichi sticks"
                min="0"
                value={hand.riichi_sticks}
                onChange={(value) => updateNumber("riichi_sticks", value)}
              />
            </div>

            <MeldBuilder
              meldType={meldType}
              selectedMeldTiles={selectedMeldTiles}
              melds={hand.melds}
              onMeldTypeChange={setMeldType}
              onAddMeld={addMeld}
              onRemoveMeld={removeMeld}
            />

            <DoraSection
              doraDraft={doraDraft}
              uraDoraDraft={uraDoraDraft}
              doraIndicators={hand.dora_indicators}
              uraDoraIndicators={hand.ura_dora_indicators}
              onDoraDraftChange={setDoraDraft}
              onUraDoraDraftChange={setUraDoraDraft}
              onAddDora={() => addIndicator("dora_indicators", doraDraft)}
              onAddUraDora={() => addIndicator("ura_dora_indicators", uraDoraDraft)}
              onRemoveDora={(index) => removeIndicator("dora_indicators", index)}
              onRemoveUraDora={(index) => removeIndicator("ura_dora_indicators", index)}
            />

            <button
              className="drawer-button"
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
            >
              <Sparkles size={18} />
              {showAdvanced ? "Hide advanced conditions" : "Show advanced conditions"}
            </button>

            {showAdvanced && (
              <AdvancedConditions
                conditions={hand.conditions}
                rules={hand.rules}
                onToggleCondition={toggleCondition}
                onToggleRule={(ruleKey) =>
                  updateHand("rules", { ...hand.rules, [ruleKey]: !hand.rules[ruleKey] })
                }
              />
            )}

            {error && (
              <div className="message error-message">
                <CircleAlert size={18} />
                <span>{error}</span>
              </div>
            )}

            <div className="actions">
              <button className="secondary-button" type="button" onClick={resetAll}>
                <RotateCcw size={18} />
                Reset
              </button>
              <button className="secondary-button" type="button" onClick={loadExampleHand}>
                <Sparkles size={18} />
                Example
              </button>
              <button className="primary-button" type="submit" disabled={isLoading}>
                <Send size={18} />
                {isLoading ? "Scoring" : "Score hand"}
              </button>
            </div>
          </form>

          <ResultPanel result={result} />
        </div>
      </section>
    </main>
  );
}

function ReadinessPanel({ messages }) {
  if (messages.length === 0) {
    return (
      <div className="message ready-message">
        <CircleCheck size={18} />
        <span>Ready to score.</span>
      </div>
    );
  }

  return (
    <div className="readiness-panel" aria-live="polite">
      <strong>Before scoring</strong>
      <ul>
        {messages.map((message) => (
          <li key={message}>{message}</li>
        ))}
      </ul>
    </div>
  );
}

function BackendBadge({ status }) {
  const label = status === "online" ? "Backend online" : status === "offline" ? "Backend offline" : "Checking";
  const icon = status === "online" ? <CircleCheck size={16} /> : <CircleAlert size={16} />;

  return (
    <div className={`backend-badge ${status}`}>
      {icon}
      <span>{label}</span>
    </div>
  );
}

function PanelTitle({ icon, title, subtitle }) {
  return (
    <div className="panel-title">
      <div className="title-icon">{icon}</div>
      <div>
        <h2>{title}</h2>
        <p>{subtitle}</p>
      </div>
    </div>
  );
}

function TileTray({ tiles, winningTile, selectedMeldTiles, onRemove, onSelectForMeld }) {
  return (
    <section className="tile-tray">
      {tiles.length === 0 ? (
        <div className="empty-state compact">Tap tiles below to build the hand</div>
      ) : (
        tiles.map((tileId, index) => {
          const selectionKey = `${tileId}-${index}`;
          const isSelected = selectedMeldTiles.some((tile) => tile.key === selectionKey);
          const isWinningTile = normalizeRedFive(tileId) === normalizeRedFive(winningTile);

          return (
            <div className={`hand-tile ${isWinningTile ? "winning" : ""}`} key={selectionKey}>
              <button
                type="button"
                onClick={() => onSelectForMeld(tileId, index)}
                className={isSelected ? "selected" : ""}
                aria-label={`Select ${getTileLabel(tileId)} hand tile ${index + 1}`}
              >
                {getTileLabel(tileId)}
              </button>
              <button type="button" className="remove-tile" onClick={() => onRemove(index)} aria-label="Remove tile">
                <X size={14} />
              </button>
            </div>
          );
        })
      )}
    </section>
  );
}

function TilePalette({ tileCounts, onAddTile }) {
  return (
    <section className="tile-palette">
      {tileGroups.map((group) => (
        <div key={group.name} className="tile-group">
          <h3>{group.name}</h3>
          <div className="tile-buttons">
            {group.tiles.map((tileId) => {
              const count = tileCounts[normalizeRedFive(tileId)] || 0;
              const disabled = count >= 4;
              return (
                <button
                  key={tileId}
                  type="button"
                  className={tileId.startsWith("0") ? "tile-button red-five" : "tile-button"}
                  disabled={disabled}
                  onClick={() => onAddTile(tileId)}
                  aria-label={`Add ${getTileLabel(tileId)}`}
                >
                  {getTileLabel(tileId)}
                </button>
              );
            })}
          </div>
        </div>
      ))}
    </section>
  );
}

function SegmentedControl({ label, value, options, onChange }) {
  return (
    <fieldset className="segment-field">
      <legend>{label}</legend>
      <div className="segment-options">
        {options.map((option) => (
          <button
            key={option.value}
            type="button"
            className={value === option.value ? "active" : ""}
            onClick={() => onChange(option.value)}
          >
            {option.label}
          </button>
        ))}
      </div>
    </fieldset>
  );
}

function SelectField({ label, value, options, onChange }) {
  return (
    <label className="field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {options.map((option) => (
          <option key={option} value={option}>
            {capitalize(option)}
          </option>
        ))}
      </select>
    </label>
  );
}

function NumberField({ label, value, min, onChange }) {
  return (
    <label className="field">
      <span>{label}</span>
      <input type="number" min={min} value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function MeldBuilder({ meldType, selectedMeldTiles, melds, onMeldTypeChange, onAddMeld, onRemoveMeld }) {
  return (
    <section className="helper-section">
      <PanelTitle
        icon={<Plus size={20} />}
        title="Called Groups"
        subtitle="Select entered tiles above, then add a chi, pon, or kan"
      />
      <div className="meld-row">
        <SelectField
          label="Group type"
          value={meldType}
          options={["chi", "pon", "kan", "closed_kan"]}
          onChange={onMeldTypeChange}
        />
        <button className="secondary-button" type="button" onClick={onAddMeld}>
          <Plus size={18} />
          Add group
        </button>
      </div>
      <div className="chip-row">
        {selectedMeldTiles.length === 0 ? (
          <span className="muted-text">No tiles selected for a called group</span>
        ) : (
          selectedMeldTiles.map((tile) => <TileChip key={tile.key} tileId={tile.id} />)
        )}
      </div>
      {melds.length > 0 && (
        <div className="meld-list">
          {melds.map((meld, index) => (
            <div key={`${meld.type}-${index}`} className="meld-item">
              <span>{formatMeldType(meld.type)}</span>
              <strong>{meld.tiles.map(getTileLabel).join(" ")}</strong>
              <button type="button" onClick={() => onRemoveMeld(index)} aria-label="Remove called group">
                <Eraser size={16} />
              </button>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function DoraSection({
  doraDraft,
  uraDoraDraft,
  doraIndicators,
  uraDoraIndicators,
  onDoraDraftChange,
  onUraDoraDraftChange,
  onAddDora,
  onAddUraDora,
  onRemoveDora,
  onRemoveUraDora,
}) {
  return (
    <section className="helper-section">
      <PanelTitle icon={<Sparkles size={20} />} title="Dora Indicators" subtitle="Add indicator tiles, not the dora tile itself" />
      <div className="meld-row">
        <TileSelect label="Dora" value={doraDraft} onChange={onDoraDraftChange} />
        <button className="secondary-button" type="button" onClick={onAddDora}>
          <Plus size={18} />
          Add dora
        </button>
      </div>
      <ChipList tiles={doraIndicators} onRemove={onRemoveDora} />

      <div className="meld-row">
        <TileSelect label="Ura dora" value={uraDoraDraft} onChange={onUraDoraDraftChange} />
        <button className="secondary-button" type="button" onClick={onAddUraDora}>
          <Plus size={18} />
          Add ura
        </button>
      </div>
      <ChipList tiles={uraDoraIndicators} onRemove={onRemoveUraDora} />
    </section>
  );
}

function TileSelect({ label, value, onChange }) {
  return (
    <label className="field">
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {allTiles.map((tileId) => (
          <option key={tileId} value={tileId}>
            {getTileLabel(tileId)}
          </option>
        ))}
      </select>
    </label>
  );
}

function ChipList({ tiles, onRemove }) {
  if (tiles.length === 0) {
    return <p className="muted-text">None added</p>;
  }

  return (
    <div className="chip-row">
      {tiles.map((tileId, index) => (
        <button key={`${tileId}-${index}`} className="chip-button" type="button" onClick={() => onRemove(index)}>
          {getTileLabel(tileId)}
          <X size={14} />
        </button>
      ))}
    </div>
  );
}

function TileChip({ tileId }) {
  return <span className="tile-chip">{getTileLabel(tileId)}</span>;
}

function AdvancedConditions({ conditions, rules, onToggleCondition, onToggleRule }) {
  return (
    <section className="advanced-panel">
      <div className="toggle-grid">
        {conditionOptions.map((condition) => (
          <label key={condition.key} className="check-row">
            <input type="checkbox" checked={Boolean(conditions[condition.key])} onChange={() => onToggleCondition(condition.key)} />
            <span>{condition.label}</span>
          </label>
        ))}
      </div>
      <div className="toggle-grid">
        <label className="check-row">
          <input type="checkbox" checked={rules.has_aka_dora} onChange={() => onToggleRule("has_aka_dora")} />
          <span>Red fives enabled</span>
        </label>
        <label className="check-row">
          <input type="checkbox" checked={rules.has_open_tanyao} onChange={() => onToggleRule("has_open_tanyao")} />
          <span>Open tanyao allowed</span>
        </label>
        <label className="check-row">
          <input type="checkbox" checked={rules.has_double_yakuman} onChange={() => onToggleRule("has_double_yakuman")} />
          <span>Double yakuman enabled</span>
        </label>
      </div>
    </section>
  );
}

function ResultPanel({ result }) {
  if (!result) {
    return (
      <aside className="result-panel empty-result">
        <PanelTitle icon={<Trophy size={20} />} title="Result" subtitle="Score appears after a valid winning hand" />
        <div className="empty-state">Waiting for hand</div>
      </aside>
    );
  }

  return (
    <aside className="result-panel">
      <PanelTitle icon={<Trophy size={20} />} title="Result" subtitle={`${result.han} han · ${result.fu} fu · ${result.limit}`} />

      <div className="score-display">
        <span>Main payment</span>
        <strong>{result.display}</strong>
      </div>

      <dl className="result-list">
        {Object.entries(result.payments).map(([name, points]) => (
          <div key={name}>
            <dt>{formatPaymentLabel(name)}</dt>
            <dd>{points.toLocaleString()} pts</dd>
          </div>
        ))}
        <div>
          <dt>Riichi sticks</dt>
          <dd>{result.riichi_bonus.toLocaleString()} pts</dd>
        </div>
        <div>
          <dt>Total received</dt>
          <dd>{result.total_points.toLocaleString()} pts</dd>
        </div>
      </dl>

      <section className="result-section">
        <h3>Yaku</h3>
        <div className="yaku-list">
          {result.yaku.map((yaku) => (
            <span key={yaku.name}>{yaku.name} · {yaku.han} han</span>
          ))}
        </div>
      </section>

      {result.fu_details.length > 0 && (
        <section className="result-section">
          <h3>Fu details</h3>
          <div className="fu-list">
            {result.fu_details.map((detail, index) => (
              <span key={`${detail.reason}-${index}`}>{detail.reason}: {detail.fu}</span>
            ))}
          </div>
        </section>
      )}
    </aside>
  );
}

function countTiles(tiles) {
  return tiles.reduce((counts, tileId) => {
    const normalId = normalizeRedFive(tileId);
    return { ...counts, [normalId]: (counts[normalId] || 0) + 1 };
  }, {});
}

function getReadinessMessages(hand) {
  const messages = [];

  if (hand.tiles.length < 14) {
    messages.push(`Add ${14 - hand.tiles.length} more tile${14 - hand.tiles.length === 1 ? "" : "s"}.`);
  }

  if (hand.tiles.length > 18) {
    messages.push("Remove tiles until the hand has 18 tiles or fewer.");
  }

  if (!hand.winning_tile) {
    messages.push("Choose which entered tile completed the hand.");
  }

  if (!hand.win_type) {
    messages.push("Choose ron or tsumo.");
  }

  if (!hand.winner_seat) {
    messages.push("Choose the winner seat wind.");
  }

  if (!hand.round_wind) {
    messages.push("Choose the round wind.");
  }

  return messages;
}

function normalizeRedFive(tileId) {
  if (tileId && tileId.startsWith("0")) {
    return `5${tileId[1]}`;
  }
  return tileId;
}

function getTileLabel(tileId) {
  const honorLabels = {
    "1z": "East",
    "2z": "South",
    "3z": "West",
    "4z": "North",
    "5z": "White",
    "6z": "Green",
    "7z": "Red",
  };

  if (honorLabels[tileId]) {
    return honorLabels[tileId];
  }

  if (tileId?.startsWith("0")) {
    return `Red 5${tileId[1]}`;
  }

  return tileId;
}

function formatMeldType(type) {
  const labels = {
    chi: "Chi",
    pon: "Pon",
    kan: "Kan",
    closed_kan: "Closed kan",
  };
  return labels[type] || type;
}

function formatPaymentLabel(name) {
  const labels = {
    discarder: "Discarder pays",
    dealer: "Dealer pays",
    each_non_dealer: "Each non-dealer pays",
  };
  return labels[name] || name;
}

function capitalize(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

export default App;
