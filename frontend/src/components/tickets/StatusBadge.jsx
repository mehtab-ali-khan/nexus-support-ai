// frontend/src/components/tickets/StatusBadge.jsx

export const TICKET_STATUSES = [
    { value: "open", label: "Open" },
    { value: "resolved", label: "Resolved" },
];

export const statusLabels = TICKET_STATUSES.reduce((labels, status) => {
    labels[status.value] = status.label;
    return labels;
}, {});

export function StatusBadge({ status }) {
    const styles = {
        open: "bg-[var(--p-soft)] text-[var(--p)] ring-1 ring-[var(--p-soft)]",
        resolved: "bg-[var(--s-soft)] text-[var(--s-mid)] ring-1 ring-[var(--g-300)]",
    };

    return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-bold capitalize tracking-wider ${styles[status] ?? styles.open}`}>
            {statusLabels[status] ?? status}
        </span>
    );
}
export function NewBadge() {
    return (
        <span className="px-2 py-0.5 rounded-full text-[10px] font-bold capitalize tracking-wider bg-[var(--warning-soft)] text-[var(--warning)]">
            unseen
        </span>
    );
}
export function StarButton({ isStarred, onClick, isLoading }) {
    return (
        <button
            type="button"
            onClick={onClick}
            disabled={isLoading}
            aria-label={isStarred ? "Unstar ticket" : "Star ticket"}
            aria-pressed={isStarred}
            className="w-8 h-8 rounded-[var(--radius-md)] flex items-center justify-center text-[var(--g-600)] hover:bg-[var(--g-200)] transition disabled:opacity-50 disabled:cursor-wait"
        >
            <svg
                width="16" height="16" viewBox="0 0 24 24"
                fill={isStarred ? "currentColor" : "none"}
                stroke="currentColor" strokeWidth="2"
                strokeLinecap="round" strokeLinejoin="round"
            >
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
        </button>
    );
}