import { FC, useState } from "react";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "./command";
import { useTopics } from "@/api/topics";
import { CommandLoading } from "cmdk";
import { useArticleStore } from "@/store";
import { useArticleTitles } from "@/api/article";
import { useNavigate } from "@tanstack/react-router";

export const SearchBar: FC = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [pages, setPages] = useState<string[]>([]);
  const topic = useArticleStore((state) => state.topic);
  const setTopic = useArticleStore((state) => state.setTopic);
  const setTitle = useArticleStore((state) => state.setTitle);
  const navigate = useNavigate();

  const { data, isSuccess } = useTopics();
  const titles = useArticleTitles(topic);

  const onSelectItem = (value: string) => {
    setPages([...pages, value]);

    if (topic) {
      setTitle(value);
      void navigate({ to: "/article" });
      return;
    }
    setTopic(value);
    setSearchQuery("");
  };

  const getSuggestionList = () => {
    const listData = topic ? titles.data : data;
    if (!listData) return;
    return (
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        {!isSuccess && <CommandLoading> Loading hot topics</CommandLoading>}
        <CommandGroup>
          {listData.map((item) => {
            return (
              <CommandItem
                onSelect={onSelectItem}
                key={`topic-${item}`}
                value={item}
              >
                <a className="hover:font-bold">{item}</a>
              </CommandItem>
            );
          })}
        </CommandGroup>
      </CommandList>
    );
  };

  return (
    <div className="w-2/4 ">
      <Command
        className=" border-2 border-solid border-black"
        onKeyDown={(e) => {
          // Escape goes to previous page
          // Backspace goes to previous page when search is empty
          if (e.key === "Escape" || (e.key === "Backspace" && !searchQuery)) {
            e.preventDefault();
            setPages((pages) => pages.slice(0, -1));
            setTopic(undefined);
          }
        }}
      >
        <CommandInput
          value={searchQuery}
          onValueChange={setSearchQuery}
          badges={pages}
          className="h-14"
          placeholder="Type a command or search..."
        />
        {isSuccess && getSuggestionList()}
      </Command>
    </div>
  );
};
