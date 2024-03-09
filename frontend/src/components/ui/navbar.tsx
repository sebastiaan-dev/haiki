import { Link } from "@tanstack/react-router";
import { FC } from "react";

export const Navbar: FC = () => {
  return (
    <nav className="flex justify-between">
      <div className="w-1">
        <h1 className="font-bold text-3xl ml-3"> Haiki </h1>
      </div>
      <div className="p-2 flex gap-4 mr-12">
        <Link to="/" className="[&.active]:font-bold text-xl">
          Search
        </Link>{" "}
        <Link to="/article" className="[&.active]:font-bold text-xl">
          Article
        </Link>
      </div>
    </nav>
  );
};
