import { useArticle } from "@/api/article";
import { Button } from "@/components/ui/button";
import { useArticleStore } from "@/store";
import { Link, createLazyFileRoute } from "@tanstack/react-router";
import { Citations } from "@/components/ui/citations";
import Markdown from "react-markdown";

export const Route = createLazyFileRoute("/article")({
  component: Article,
});

function Article() {
  const title = useArticleStore((state) => state.title);
  const topic = useArticleStore((state) => state.topic);

  const selectedArticle = title && topic;

  const { data, isError } = useArticle(topic, title);

  if (isError) return <>Oeps</>;

  if (!selectedArticle)
    return (
      <div className="flex flex-row justify-center">
        <Button>
          <Link to="/">Please select a article</Link>
        </Button>
      </div>
    );

  return (
    <div className="flex flex-row justify-center">
      <div className="flex flex-col mt-20 w-2/4 h-full items-center">
        <Markdown
          className="mb-10"
          components={{
            h1(props) {
              return (
                <h1
                  className="text-4xl font-bold mb-5 tracking-wider"
                  {...props}
                />
              );
            },
            h2(props) {
              return (
                <div>
                  <h2 className="text-4xl mt-10 " {...props} />
                </div>
              );
            },
            p(props) {
              return (
                <div>
                  <p className="text-xl font-medium mt-5" {...props} />
                </div>
              );
            },
            ol(props) {
              return (
                <div>
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
        <Citations />
      </div>
    </div>
  );
}
