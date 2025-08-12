import React, { useMemo, useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { useTable, useFilters, useGlobalFilter } from 'react-table';
import { useNavigate } from 'react-router-dom';

function DefaultColumnFilter({
  column: { filterValue, preFilteredRows, setFilter },
}) {
  const count = preFilteredRows.length;
  return (
    <input
      value={filterValue || ''}
      onChange={(e) => setFilter(e.target.value || undefined)}
      placeholder={`Search ${count} records...`}
    />
  );
}

function globalFilter(rows, ids, filterValue) {
  return rows.filter((row) => {
    const rowValue = row.values['title'] ? row.values['title'].toString().toLowerCase() : '';
    return rowValue.includes(filterValue.toLowerCase());
  });
}

function RedditPosts({ showActions = true }) {
  const navigate = useNavigate();
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('/api/posts', { withCredentials: true })
      .then((response) => {
        const transformedData = response.data.map((post) => ({
          ...post,
          title: post.title || '', // Ensure title always has a default value
          date: post.timestamp,
          score: post.upvotes - post.downvotes,
          url: post.permalink,
          sentiment: post.sentiment_score
        }));
        setPosts(transformedData);
        setLoading(false);
      })
      .catch((error) => {
        if (error.response) {
          console.error('Error fetching data:', error);
          setError(`HTTP error! Status: ${error.response.status}`);
        } else if (error.request) {
          setError('No response received from the server');
        } else {
          setError(error.message);
        }
        setLoading(false);
      });
  }, []);

  const handleEdit = useCallback((firebaseId, newValue, columnId) => {
    axios.put(`/api/posts/${firebaseId}`, { [columnId]: newValue })
      .then(() => {
        setPosts((prevPosts) =>
          prevPosts.map((post) =>
            post.id === firebaseId ? { ...post, [columnId]: newValue } : post
          )
        );
      })
      .catch((error) => {
        console.error('Error updating post:', error);
      });
  }, []);

  const handleDelete = useCallback((firebaseId) => {
    axios.delete(`/api/posts/${firebaseId}`)
      .then(() => {
        setPosts((prevPosts) => prevPosts.filter((post) => post.id !== firebaseId));
      })
      .catch((error) => {
        console.error('Error deleting post:', error);
      });
  }, []);

  const columns = useMemo(() => [
    {
      Header: 'Title',
      accessor: 'title',
      width: '30%',
    },
    {
      Header: 'Body',
      accessor: 'body',
      width: '30%',
      Cell: ({ value }) => (
        <span style={{ fontSize: '12px' }}>{value}</span>
      ),
    },
    {
      Header: 'Subreddit',
      accessor: 'subreddit',
      width: '10%',
    },
    {
      Header: 'Date',
      accessor: 'date',
      Filter: DefaultColumnFilter,
      width: '10%',
    },
    {
      Header: 'Sentiment Score',
      accessor: 'sentiment',
      width: '5%',
    },
    {
      Header: (
        <span role="img" aria-label="upvote">
          &#x1F44D;
        </span>
      ),
      accessor: 'upvotes',
      width: '5%',
    },
    {
      Header: (
        <span role="img" aria-label="downvote">
          &#x1F44E;
        </span>
      ),
      accessor: 'downvotes',
      width: '5%',
    },
    {
      Header: 'Score',
      accessor: 'score',
      Filter: DefaultColumnFilter,
      width: '5%',
    },
    {
      Header: 'URL',
      accessor: 'url',
      Cell: ({ value }) => (
        <a href={value} target="_blank" rel="noopener noreferrer">
          Link
        </a>
      ),
      width: '5%',
    },
    {
      Header: 'Actions',
      id: 'actions',
      Cell: ({ row }) => showActions ? (
        <div>
          <button onClick={() => navigate(`/edit/${row.original.id}`)} style={{ marginRight: '5px' }}>Edit</button>
          <button onClick={() => handleDelete(row.original.id)}>Delete</button>
        </div>
      ) : null,
      width: '5%',
    }
  ], [handleDelete, navigate, showActions]);
  

  const tableInstance = useTable(
    {
      columns,
      data: posts,
      defaultColumn: { Filter: DefaultColumnFilter }, // Apply DefaultColumnFilter globally
      globalFilter: globalFilter,
    },
    useFilters,
    useGlobalFilter
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = tableInstance;

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (posts.length === 0) return <div>No posts found.</div>;

  return (
    <div>
      <h1>Reddit Posts</h1>
      <table {...getTableProps()} style={{ borderCollapse: 'collapse', width: '100%', border: '1px solid black', tableLayout: 'fixed' }}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()} style={{ border: '1px solid black', padding: '8px', width: column.width }}>
                  {column.render('Header')}
                  {column.canFilter ? column.render('Filter') : null}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()} style={{ border: '1px solid black' }}>
                {row.cells.map((cell) => (
                  <td {...cell.getCellProps()} style={{ border: '1px solid black', padding: '8px', width: cell.column.width }}>
                    {cell.isEditing ? (
                      <input
                        type="text"
                        value={cell.value}
                        onChange={(e) => {
                          const newValue = e.target.value;
                          handleEdit(row.original.id, newValue, cell.column.id);
                        }}
                      />
                    ) : cell.render('Cell')}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default RedditPosts;
