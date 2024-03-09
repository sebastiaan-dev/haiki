import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/article")({
  component: Article,
});

function Article() {
  return <div className="p-2">Hello from About!</div>;
}
