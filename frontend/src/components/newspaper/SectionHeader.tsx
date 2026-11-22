export default function SectionHeader({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="my-8">
      <div className="flex items-center gap-4">
        <h2 className="newspaper-title text-2xl md:text-3xl font-extrabold uppercase tracking-wider text-ink dark:text-ink-dark whitespace-nowrap">
          {title}
        </h2>
        <div className="flex-1 h-[2px] bg-stone-800 dark:bg-stone-300"></div>
      </div>
      {subtitle && (
        <p className="text-xs uppercase tracking-widest text-stone-500 dark:text-stone-400 mt-1 font-sans">
          {subtitle}
        </p>
      )}
    </div>
  );
}
