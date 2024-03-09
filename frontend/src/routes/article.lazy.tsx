import { useArticle } from "@/api/article";
import { createLazyFileRoute } from "@tanstack/react-router";
import Markdown from "react-markdown";

export const Route = createLazyFileRoute("/article")({
  component: Article,
});

function Article() {
  const { data, isError } = useArticle();

  if (isError) return "Failed to load article";

  return (
    <div className="flex flex-row justify-center">
      <div className="flex flex-col mt-20 w-2/4 h-full items-center">
        <Markdown
          components={{
            h1(props) {
              return <h1 className="text-4xl font-bold " {...props} />;
            },
            h2(props) {
              return (
                <div className="w-4/5">
                  <h2 className="text-4xl mt-10 " {...props} />
                </div>
              );
            },
            p(props) {
              return (
                <div className="w-4/5">
                  <p className="text-xl font-medium mt-5" {...props} />
                </div>
              );
            },
            ol(props) {
              return (
                <div className="w-4/5">
                  <ol className="text-xl font-medium mt-5" {...props} />
                </div>
              );
            },
            li(props) {
              return (
                <div className="w-4/5">
                  <li className="text-xl font-medium mt-5" {...props} />
                </div>
              );
            },
          }}
        >
          {data}
        </Markdown>
      </div>
    </div>
  );
}
