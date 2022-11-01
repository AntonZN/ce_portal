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
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: '/organization/api/v1/employees/search?query=%QUERY',
        wildcard: '%QUERY'
    }
});

states.initialize();


$('.the-basics .typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'states',
        display: 'name',
        source: states.ttAdapter(),
        templates: {
            empty: [
                '<div class="empty-message">',
                'По вашему запросу нет результатов!',
                '</div>'
            ].join('\n'),
            suggestion: function (data) {
                var avatar = "/static/assets/images/smlogo.jpg"
                if (data.avatar){
                    avatar = data.avatar
                }
                return '<a href=' + '"/organization/employees/' + data.pk +'" class="man-section"><div class="image-section"><img src=' + avatar + '></div><div class="description-section"><h4>' + data.name + '</h4><span>' + data.position + '</span></div></a>';
            }
        },
    });