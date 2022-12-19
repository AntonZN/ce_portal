var substringMatcher = function (strs) {
    return function findMatches(q, cb) {
        var matches, substringRegex;
        matches = [];
        substrRegex = new RegExp(q, 'i');
        $.each(strs, function (i, str) {
            if (substrRegex.test(str)) {
                matches.push(str);
            }
        });
        cb(matches);
    };
};


var states = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('title'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: '/organization/api/v1/search?query=%QUERY',
        wildcard: '%QUERY'
    }
});

states.initialize();


$('.the-basics .typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 5
    },
    {
        name: 'states',
        display: 'title',
        limit: 100,
        source: states.ttAdapter(),
        templates: {
            empty: [
                '<div class="empty-message">',
                'По вашему запросу нет результатов!',
                '</div>'
            ].join('\n'),
            suggestion: function (data) {
                console.log(data.url)

                return '<a href="' + data.url +'" class="man-section"><div class="description-section"><h4>' + data.title + '</h4><span>' + data.type + '</span></div></a>';
            }
        },
    });