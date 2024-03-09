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

export const SearchBar: FC = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [pages, setPages] = useState<string[]>([]);
  const page = pages[pages.length - 1];
  const topic = useArticleStore((state) => state.topic);
  const setTopic = useArticleStore((state) => state.setTopic);

  const { data, isSuccess } = useTopics();
  const titles = useArticleTitles(topic);

  const onSelectItem = (value: string) => {
    setPages([...pages, value]);
    setTopic(value);
  };

  const getSuggestionList = () => {
    if (!isSuccess) return;
    return (
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        {!isSuccess && <CommandLoading> Loading hot topics</CommandLoading>}
        <CommandGroup heading={page}>
          {data.map((item) => {
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
    <div className="  w-2/4 ">
      <Command
        className=" border-2 border-solid border-black"
        onKeyDown={(e) => {
          // Escape goes to previous page
          // Backspace goes to previous page when search is empty
          if (e.key === "Escape" || (e.key === "Backspace" && !searchQuery)) {
            e.preventDefault();
            setPages((pages) => pages.slice(0, -1));
          }
        }}
      >
        <CommandInput
          value={searchQuery}
          onValueChange={setSearchQuery}
          className="h-14"
          placeholder="Type a command or search..."
        />
        {isSuccess && getSuggestionList()}
      </Command>
    </div>
  );
};
