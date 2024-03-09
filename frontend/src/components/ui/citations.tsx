import { useArticle } from "@/api/article";
import "@citation-js/plugin-doi";
import cite from "citation-js";
import { useEffect, useState } from "react";

export const Citations = () => {
  const { data } = useArticle("supplement", "matcha", false);
  const [cites, setCites] = useState<string[]>([]);

  useEffect(() => {
    if (!data) return;

    const promises = [...new Set(data.citations)].map((data) =>
      cite.async(data)
    );
    Promise.all(promises).then((resolved) => {
      setCites(resolved);
    });
  }, [data]);

  return (
    <div>
      {cites.map((c) => (
        <div className="pt-2 pb-2">
          <div
            dangerouslySetInnerHTML={{
              __html: c.format("bibliography", {
                format: "html",
                template: "apa",
                lang: "en-US",
              }),
            }}
          />
        </div>
      ))}
    </div>
  );
};
