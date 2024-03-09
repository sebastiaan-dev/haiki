import { Navbar } from "@/components/ui/navbar";
import { createRootRoute, Outlet } from "@tanstack/react-router";

export const Route = createRootRoute({
  component: () => (
    <div className="w-svh h-svh">
      <Navbar />
      <hr />
      <Outlet />
    </div>
  ),
});
