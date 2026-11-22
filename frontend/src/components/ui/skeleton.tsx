import { cn } from "@/lib/utils";

export function Skeleton({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded bg-stone-200 dark:bg-stone-800", className)}
      {...props}
    />
  );
}

export function ArticleCardSkeleton() {
  return (
    <div className="p-4 border border-stone-200 dark:border-stone-800 rounded bg-white dark:bg-stone-900 space-y-3">
      <Skeleton className="h-4 w-20" />
      <Skeleton className="h-6 w-full" />
      <Skeleton className="h-4 w-3/4" />
      <div className="pt-2 flex justify-between">
        <Skeleton className="h-3 w-24" />
        <Skeleton className="h-3 w-16" />
      </div>
    </div>
  );
}
