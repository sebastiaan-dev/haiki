import { SearchBar } from "@/components/ui/search-bar";
import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <div className="h-full w-full flex flex-col justify-center gap-40 items-center">
      <div className="flex flex-col justify-center items-center">
        <h1 className="font-bold font-DraftingMono text-8xl">
          Welcome to Haiki
        </h1>
        <h2>Find all your information based on facts</h2>
      </div>
      <SearchBar />
    </div>
  );
}
