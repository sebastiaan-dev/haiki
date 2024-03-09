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

export const SearchBar: FC = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const { data, isSuccess, isError } = useTopics();

  if (isError) return <>"Failed"</>;

  return (
    <div className="  w-2/4 ">
      <Command className=" border-2 border-solid border-black">
        <CommandInput
          value={searchQuery}
          onValueChange={setSearchQuery}
          className="h-14"
          placeholder="Type a command or search..."
        />
        <CommandList>
          <CommandEmpty>No results found.</CommandEmpty>
          {!isSuccess && <CommandLoading> Loading hot topics</CommandLoading>}
          <CommandGroup heading="Hot topics">
            {data?.map((item) => {
              return (
                <CommandItem key={`topic-${item}`} value={item}>
                  <a className="hover:font-bold">{item}</a>
                </CommandItem>
              );
            })}
          </CommandGroup>
        </CommandList>
      </Command>
    </div>
  );
};
