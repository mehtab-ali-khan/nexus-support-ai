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