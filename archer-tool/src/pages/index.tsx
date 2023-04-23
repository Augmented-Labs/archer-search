import Image from "next/image";
import { Inter } from "next/font/google";
import { FiArrowDown, FiChevronDown, FiSearch } from "react-icons/fi";
import { useRef, useState } from "react";
import {
  Menu,
  MenuButton,
  MenuDivider,
  MenuItem,
  MenuList,
  Spinner,
} from "@chakra-ui/react";
import axios from "axios";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [searchType, setSearchType] = useState(null);
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState("");

  const [postData, setPostData] = useState({});

  const getPosts = async () => {
    setLoading(true);
    const results = await axios.post("/api/linkedin-posts", {
      query,
      url,
      searchType,
    });
    setPostData(results.data);
    setLoading(false);
  };
  console.log(postData);
  return (
    <div className=" min-h-screen bg-slate-100 overflow-hidden">
      <div className="w-full h-full flex flex-col justify-center items-center pt-36 px-80">
        <div className="font-playfair font-bold text-6xl mb-8 text-primary">
          Archer
        </div>
        <div className="flex space-x-4 w-full px-24">
          <Menu>
            <MenuButton className="bg-white px-4 py-1 border border-primary rounded-sm w-fit whitespace-nowrap">
              <div className="flex items-center">
                {searchType ? searchType : "Choose Search Type"}
                <span className="ml-2">
                  <FiChevronDown />
                </span>
              </div>
            </MenuButton>
            <MenuList>
              <MenuItem onClick={() => setSearchType("Company Search")}>
                Company
              </MenuItem>
              <MenuItem onClick={() => setSearchType("Individual Search")}>
                Individual Profile
              </MenuItem>
            </MenuList>
          </Menu>
          <input
            className="border w-full px-2 py-1 focus:outline-none"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder={
              searchType === null
                ? "Select a search type first"
                : searchType === "Individual Search"
                ? "Type in a Linkedin post"
                : "Enter a company domain"
            }
          />
        </div>
        <div className="flex w-full">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={
              searchType === null
                ? "Select a Search Type first"
                : "e.g. mentions cybersecurity OR red teaming"
            }
            disabled={searchType === null}
            className="border-2 px-4 py-2 rounded-2xl mt-4 w-full focus:ring-0 focus:outline-none border-r-0 rounded-r-none"
          />
          <div
            className={`border-2 px-4 py-2 ${
              searchType === null ? "bg-[#F0F3F6]" : "bg-white"
            } rounded-2xl w-full] mt-4 focus:ring-0 focus:outline-none border-l-0 rounded-l-none`}
          >
            <button
              className="bg-primary text-white py-2 px-3 rounded-lg"
              onClick={getPosts}
            >
              {loading ? (
                <Spinner w="18px" h="18px" />
              ) : (
                <FiSearch size={"20px"} />
              )}
            </button>
          </div>
        </div>
        {postData && postData.searchType === "Individual Search" && (
          <div className="mt-4 w-full mb-8">
            <div className="font-bold text-center">Results</div>
            <div className="mt-4 border bg-white px-4 py-2">
              <span className="font-bold">Profile</span>
              <a
                href={postData.linkedin_profile_url}
                className="underline ml-2"
              >
                {postData.linkedin_profile_url}
              </a>
              <div className="font-bold mt-4">Relevant Posts</div>
              {postData.relevant_posts.map((item, idx) => {
                return (
                  <div key={idx} className="mt-1 bg-slate-100 px-2 py-2 my-2">
                    <div className="text-primary font-bold">
                      {item.time} ago -{" "}
                      <span className="font-normal hover:underline">
                        <a
                          target="_blank"
                          rel="noopener noreferrer"
                          href={item.url}
                        >
                          Link
                        </a>
                      </span>
                    </div>
                    {item.text}
                  </div>
                );
              })}
            </div>
          </div>
        )}
        {postData && postData?.searchType === "Company Search" && (
          <div className="mt-4 w-full mb-8">
            <div className="font-bold text-center">Results</div>
            {postData?.result
              .filter((i) => i.relevant_posts.length > 0)
              .map((person, idx) => {
                return (
                  <div key={idx} className="mt-4 border bg-white px-4 py-2">
                    <span className="font-bold">Profile</span>
                    <a
                      href={person.linkedin_profile_url}
                      className="underline ml-2"
                    >
                      {person.linkedin_profile_url}
                    </a>
                    <div>
                      {person.name} - {person.title}
                    </div>
                    <div className="font-bold mt-4">Relevant Posts</div>
                    {person.relevant_posts.map((item, idx) => {
                      return (
                        <div
                          key={idx}
                          className="mt-1 bg-slate-100 px-2 py-2 my-2"
                        >
                          <div className="text-primary font-bold">
                            {item.time} ago -{" "}
                            <span className="font-normal hover:underline">
                              <a
                                target="_blank"
                                rel="noopener noreferrer"
                                href={item.url}
                              >
                                Link
                              </a>
                            </span>
                          </div>
                          {item.text}
                        </div>
                      );
                    })}
                  </div>
                );
              })}
          </div>
        )}
      </div>
    </div>
  );
}
